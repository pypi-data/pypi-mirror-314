from sqlalchemy.orm import make_transient
from waiting import wait

from fild_compare import compare
from fild_db.client import DbClient
from fild_db.types.model import DbModel


DEFAULT_DB_TIMEOUT = 3


def to_dict(model_record, filter_none=True):
    d = {}

    for column in model_record.__table__.columns:
        column_name = column.name

        if column_name == 'global':
            column_name = 'is_global'

        value = getattr(model_record, column_name)

        if filter_none and value is None:
            continue

        d[column_name] = value

    return d


class Database:
    _no_db_mode = False

    def __init__(self, client_name, client):
        self.db = DbClient(client_name=client_name, client=client)

    def enable_no_db_mode(self):
        self._no_db_mode = True

    def reset_mode(self):
        self._no_db_mode = False

    def _get_records(self, model, *criteria, **kwargs):
        order_by = kwargs.pop('order_by', None)
        query = self.db.connection.query(model)

        if criteria:
            data = query.filter(*criteria).filter_by(**kwargs).order_by(
                order_by
            ).all()
        else:
            data = query.filter_by(**kwargs).order_by(order_by).all()

        self.db.connection.close()
        return data

    def get_record(self, model, *criteria, **kwargs):
        return self.get_records(model, *criteria, **kwargs)[0]

    def get_records_nowait(self, model, *criteria, **kwargs):
        return [
            model(is_custom=True).with_values(to_dict(rec))
            for rec in self._get_records(model.__table__, *criteria, **kwargs)
        ]

    def get_records(self, model, *criteria, **kwargs):
        sleep_seconds = kwargs.pop('sleep_seconds', 0)
        timeout_seconds = kwargs.pop('timeout_seconds', None)

        def filter_records():
            return [
                model(is_custom=True).with_values(to_dict(rec))
                for rec in self._get_records(
                    model.__table__, *criteria, **kwargs
                )
            ]

        return wait(
            filter_records,
            waiting_for=f'records from {model.get_table_name()} by: {kwargs}',
            timeout_seconds=timeout_seconds or DEFAULT_DB_TIMEOUT,
            sleep_seconds=sleep_seconds
        )

    def insert(self, record):
        if self._no_db_mode:
            return None

        model = record
        record = model.to_table_record()

        self.db.connection.add(record)
        self.db.connection.commit()
        # refresh() gets actual record state after commit
        # (needed to make_transient)
        # make_transient unbinds model from slqalchemy session
        self.db.connection.refresh(record)
        make_transient(record)
        self.db.connection.close_all()

        return model.__class__(is_custom=model.is_custom).with_values(
            to_dict(record)
        )

    def insert_records(self, records):
        if self._no_db_mode:
            return

        for record in records:
            record = record.to_table_record()
            self.db.connection.add(record)
            self.db.connection.flush()

        self.db.connection.commit()
        self.db.connection.close_all()

    def delete(self, model, *criteria, **kwargs):
        """
        :param criteria: Conditional criteria to delete records, e.g.:
          MyClass.name == 'some name'
          MyClass.id > 5,
          MyClass.field.in_([1, 2, 3])
        :param kwargs: Key-value conditions, e.g.:
          name='some name'
          id=5
        """
        query = self.db.connection.query(model.__table__)

        if criteria:
            query = query.filter(*criteria)
        else:
            query = query.filter_by(**kwargs)

        query.delete(synchronize_session=False)
        self.db.connection.commit()
        self.db.connection.close_all()

    def update(self, model, new_values, *criteria, **kwargs):
        """
        Note: new_values - a dictionary where keys are column names,
         values - corresponding values to set.
        """
        query = self.db.connection.query(model.__table__)

        if criteria:
            records = query.filter(*criteria)
        else:
            records = query.filter_by(**kwargs)

        records.update(new_values, synchronize_session='fetch')
        self.db.connection.commit()
        self.db.connection.close_all()

    def cascade_delete(self, model):
        sql = f'TRUNCATE {model.__table__.__tablename__} CASCADE;'
        self.db.connection.execute(sql)
        self.db.connection.commit()
        self.db.connection.close_all()

    def verify_no_record(self, model, *criteria, **kwargs):
        data = self._get_records(model.__table__, *criteria, **kwargs)
        assert not data, (
            f'Unexpected {model.get_table_name()} record by: {kwargs}'
        )

    def verify_no_record_with_wait(self, model, *criteria, **kwargs):
        wait(
            lambda: not self._get_records(model.__table__, *criteria, **kwargs),
            waiting_for=f'no {model.get_table_name()} records by: {kwargs}',
            timeout_seconds=DEFAULT_DB_TIMEOUT,
            sleep_seconds=0
        )

    @staticmethod
    def verify_record(actual: DbModel, expected: DbModel, rules=None):
        compare(
            actual=actual.value,
            expected=expected.value,
            rules=rules
        )

    @staticmethod
    def verify_records(actual: [DbModel], expected: [DbModel], rules=None):
        target_name = ''

        if actual:
            target_name = actual[0].get_table_name()
        elif expected:
            target_name = expected[0].get_table_name()

        actual_data = [item.value for item in actual]
        expected_data = [item.value for item in expected]
        compare(
            actual=actual_data,
            expected=expected_data,
            target_name=f'{target_name} records',
            rules=rules
        )

    def trunc_all_tables(self, exclude=None):
        self.db.trunc_all_tables(exclude_tables=exclude) # pylint: disable=no-member
