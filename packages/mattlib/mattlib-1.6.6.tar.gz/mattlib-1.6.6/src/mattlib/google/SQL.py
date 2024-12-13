import sqlalchemy

def create_url(db_name, db_host, db_user, db_pass, in_cloud):
#   Equivalent URL:
#   mysql+pymysql://<db_user>:<db_pass>@/<db_name>?unix_socket=<socket_path>/<cloud_sql_instance_name>
    if in_cloud:
        db_socket_dir = "/cloudsql"
        instance_connection_name = os.getenv("INSTANCE_CONNECTION_NAME")
        return sqlalchemy.engine.url.URL.create(
            drivername="mysql+pymysql",
            username=db_user,  # e.g. "my-database-user"
            password=db_pass,  # e.g. "my-database-password"
            database=db_name,  # e.g. "my-database-name"
            host=db_host,
            query={
                "unix_socket": "{}/{}".format(
                db_socket_dir,  # e.g. "/cloudsql"
                instance_connection_name)  # i.e "<PROJECT-NAME>:<INSTANCE-REGION>:<INSTANCE-NAME>"
                }
        )
    else:
        return sqlalchemy.engine.url.URL.create(
            drivername="mysql+pymysql",
            username=db_user,  # e.g. "my-database-user"
            password=db_pass,  # e.g. "my-database-password"
            database=db_name,  # e.g. "my-database-name"
            host=db_host,
        )


# criada a partir do documento: https://cloud.google.com/sql/docs/mysql/connect-functions#configure
def get_engine(db_name, db_host, db_user, db_pass, in_cloud):
    url = create_url(db_name, db_host, db_user, db_pass, in_cloud)

    engine = sqlalchemy.create_engine(
        url
    )
    return engine
