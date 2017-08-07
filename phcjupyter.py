from tornado import gen
from jupyterhub.auth import Authenticator
import pymysql, hashlib, random
import os, pwd, shutil

# forked 8/1/17 from sqlauth.py
class MySQLAuthenticator(Authenticator):
    # TODO: consider modularity of jupyterhub fork

    @gen.coroutine
    def authenticate(self, handler, data):
        cfg = self.config.PHCHandler
        db = pymysql.connect(db=cfg.phc_db, host=cfg.phc_db_host)

        # db = pymysql.connect(read_default_file='.my.cnf', db='phcwebusers')
        # db = pymysql.connect("example.db")

        sql = "SELECT Folder,passwd FROM users WHERE Email = '{}'"\
                .format(data['username'])

        with db.cursor() as cur:
            cur.execute(sql)
            folder,pwd = cur.fetchone()

            if tup is not None\
                and folder is not ''\
                and self.matches_token(data['password'], pwd):
                # slice folder secret to make valid uname
                uname = "_"+folder[0:30]

                try:
                    user = pwd.getpwnam(uname) # FIXME: handle (unlikely) collisions
                except KeyError:
                    # create user if none exists
                    entrop = hex(random.getrandbits(128)) # random password, which su ignores
                    os.system("useradd -p {} {}".format(entrop, uname))
                    user = pwd.getpwnam(uname)

                self.attach_sage(user)
                return uname # data['username']
                    # dict(name=fold, auth_state=dict(pwd=word)) # needs version 0.8.0

    def matches_token(self, input, goal):
        s = hashlib.sha1()
        s.update(input.encode('utf-8')) # guaranteed to not return None
        return s.hexdigest() == goal

    def attach_sage(self, user):
        # VERIFY: single-user server launches with EUID == UID set here?
        sage = os.path.join(user.pw_dir, '.sage')
        uid = user.pw_uid; gid = user.pw_gid

        # give new user permissions to their .sage
        os.chown(sage, uid, gid)
        for root, dirs, files in os.walk(sage):
            for u in dirs: os.chown(os.path.join(root, u), uid, gid)
            for u in files: os.chown(os.path.join(root, u), uid, gid)

        # add magics to sage
        base_st = os.path.normpath('/home/jupyterhub/startup')
        ipy_st = os.path.join(user.pw_dir,
                ".sage/ipython-5.0.0/profile_default/startup")
        os.makedirs(ipy_st, exist_ok=True) # VERIFY: needs root?
        
        for f in os.listdir(base_st):
            # clobbers destination! (TODO: also clean destination)
            shutil.copyfile(os.path.join(base_st, f),
                            os.path.join(ipy_st, f))
