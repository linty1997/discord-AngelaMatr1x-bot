from .models import Session, User, Log
from datetime import datetime, timedelta
import uuid


class BaseDB:
    def __init__(self):
        self.db = Session().get_db()
        self.now_time = datetime.utcnow()
        self.now_timestamp = datetime.utcnow().timestamp()


class UserDB(BaseDB):
    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx
        self.check_in_fraction = 5  # TODO: 簽到獎勵
        self.user = None

    async def get_user(self, user_id):
        user = self.db.query(User).filter(User.id == user_id).first()
        return user if user else None

    async def get_users(self):
        return self.db.query(User).all()

    async def get_user_fractions(self, user_id):
        user = await self.get_user(user_id)
        if user is None:
            return 0
        return user.fraction

    async def get_leader_board(self, old=False):
        users = await self.get_users()
        data = sorted(users, key=lambda user: user.old_fraction if old else user.fraction, reverse=True)
        return data

    async def crate_user(self, user_id, user_name, old_fraction, fraction):
        user = User(id=user_id, name=user_name, old_fraction=old_fraction,
                    fraction=fraction, update_time=self.now_time)
        self.db.add(user)
        self.db.commit()
        return user

    async def check_user_in_db(self, user_id, user_name, fraction=0):
        user = await self.get_user(user_id)
        if user is None:
            fraction = 0 if fraction < 0 else fraction
            return await self.crate_user(user_id, user_name, 0, fraction)
        return user

    async def update_user_fraction(self, user, fraction):
        self.user = user
        user_name = f"{self.user.name}#{self.user.discriminator}"
        user = await self.check_user_in_db(self.user.id, user_name, fraction)
        if user is None:
            return False

        user.fraction += fraction
        user.fraction = 0 if user.fraction < 0 else user.fraction

        user.name = user_name
        user.update_time = self.now_time
        self.db.commit()
        return user

    async def update_user_sign_in(self, user):
        self.user = user
        user_name = f"{self.user.name}#{self.user.discriminator}"
        user = await self.check_user_in_db(self.user.id, user_name)
        yesterday = self.now_time.date() - timedelta(days=1)

        if user is None:
            return 'Unknown error occurred, failed to create user.', 0, "Null"
        if user.last_sign_in is not None and user.last_sign_in.date() == self.now_time.date():
            return 'You have already checked in today.', 0, user.fraction
        if user.last_sign_in is None or user.last_sign_in is not None and user.last_sign_in and user.last_sign_in.date() != yesterday:
            user.consecutive_sign_in = 1
        else:
            user.consecutive_sign_in += 1
        user.fraction += self.check_in_fraction
        user.last_sign_in = self.now_time
        self.db.commit()
        await LogDB().add_log(self.user.id, event='Check-in')  # TODO: 紀錄簽到事件
        return f'Daily check-in completed.', self.check_in_fraction, user.fraction

    async def settle_accounts(self, days, award):
        users = await self.get_users()

        for user in users:
            if user.consecutive_sign_in >= days:  # TODO: 連續簽到天數大於等於設定天數給予獎勵分
                user.fraction += award

            user.old_fraction = user.fraction  # TODO: 將目前分數轉移至舊分數給排行榜使用
            user.fraction = 0  # TODO: 結算完後將分數歸零
            user.consecutive_sign_in = 0  # TODO: 將連續簽到天數歸零

        self.db.commit()
        return True


class LogDB(BaseDB):
    def __init__(self):
        super().__init__()

    async def add_log(self, user_id, event):
        log = Log(id=uuid.uuid4(), event_time=self.now_time, user_id=user_id, event=event)
        self.db.add(log)
        self.db.commit()
        return log

    async def get_logs(self, user_id, event=None):
        logs = self.db.query(Log).filter(Log.user_id == user_id).all()
        if event and logs:
            logs = [log for log in logs if log.event == event]
        return logs if logs else None
