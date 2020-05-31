# coding: utf-8
from sqlalchemy import Column, Float, String
from sqlalchemy.dialects.mysql import BIGINT, DATETIME, INTEGER, LONGTEXT, SMALLINT, TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class AuthGroup(Base):
    __tablename__ = 'auth_group'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(150), nullable=False)


class AuthGroupPermission(Base):
    __tablename__ = 'auth_group_permissions'

    id = Column(INTEGER(11), primary_key=True)
    group_id = Column(INTEGER(11), nullable=False)
    permission_id = Column(INTEGER(11), nullable=False)


class AuthPermission(Base):
    __tablename__ = 'auth_permission'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(255), nullable=False)
    content_type_id = Column(INTEGER(11), nullable=False)
    codename = Column(String(100), nullable=False)


class AuthUser(Base):
    __tablename__ = 'auth_user'

    id = Column(INTEGER(11), primary_key=True)
    password = Column(String(128), nullable=False)
    last_login = Column(DATETIME(fsp=6))
    is_superuser = Column(TINYINT(1), nullable=False)
    username = Column(String(150), nullable=False)
    first_name = Column(String(30), nullable=False)
    last_name = Column(String(150), nullable=False)
    email = Column(String(254), nullable=False)
    is_staff = Column(TINYINT(1), nullable=False)
    is_active = Column(TINYINT(1), nullable=False)
    date_joined = Column(DATETIME(fsp=6), nullable=False)


class AuthUserGroup(Base):
    __tablename__ = 'auth_user_groups'

    id = Column(INTEGER(11), primary_key=True)
    user_id = Column(INTEGER(11), nullable=False)
    group_id = Column(INTEGER(11), nullable=False)


class AuthUserUserPermission(Base):
    __tablename__ = 'auth_user_user_permissions'

    id = Column(INTEGER(11), primary_key=True)
    user_id = Column(INTEGER(11), nullable=False)
    permission_id = Column(INTEGER(11), nullable=False)


class AuthtokenToken(Base):
    __tablename__ = 'authtoken_token'

    key = Column(String(40), primary_key=True)
    created = Column(DATETIME(fsp=6), nullable=False)
    user_id = Column(INTEGER(11), nullable=False)


class DatasetsDatasetsinfo(Base):
    __tablename__ = 'datasets_datasetsinfo'

    id = Column(INTEGER(11), primary_key=True)
    dataset_name = Column(String(255), nullable=False)
    dataset_time = Column(DATETIME(fsp=6), nullable=False)
    dataset_status = Column(INTEGER(11), nullable=False)
    dataset_fileaddr = Column(String(255))
    dataset_ratio = Column(String(255), nullable=False)
    dataset_describe = Column(String(255), nullable=False)
    dataset_part_id = Column(INTEGER(11), nullable=False)


class DjangoAdminLog(Base):
    __tablename__ = 'django_admin_log'

    id = Column(INTEGER(11), primary_key=True)
    action_time = Column(DATETIME(fsp=6), nullable=False)
    object_id = Column(LONGTEXT)
    object_repr = Column(String(200), nullable=False)
    action_flag = Column(SMALLINT(5), nullable=False)
    change_message = Column(LONGTEXT, nullable=False)
    content_type_id = Column(INTEGER(11))
    user_id = Column(INTEGER(11), nullable=False)


class DjangoContentType(Base):
    __tablename__ = 'django_content_type'

    id = Column(INTEGER(11), primary_key=True)
    app_label = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)


class DjangoMigration(Base):
    __tablename__ = 'django_migrations'

    id = Column(INTEGER(11), primary_key=True)
    app = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    applied = Column(DATETIME(fsp=6), nullable=False)


class DjangoSession(Base):
    __tablename__ = 'django_session'

    session_key = Column(String(40), primary_key=True)
    session_data = Column(LONGTEXT, nullable=False)
    expire_date = Column(DATETIME(fsp=6), nullable=False)


class ModelmanagementDatasettestmodel(Base):
    __tablename__ = 'modelmanagement_datasettestmodel'

    id = Column(INTEGER(11), primary_key=True)
    test_time = Column(DATETIME(fsp=6), nullable=False)
    dataset_list = Column(String(255), nullable=False)
    accuracy_rate = Column(Float(asdecimal=True), nullable=False)
    testing_model_id = Column(INTEGER(11), nullable=False)


class ModelmanagementDatasettrainingmodel(Base):
    __tablename__ = 'modelmanagement_datasettrainingmodel'

    id = Column(INTEGER(11), primary_key=True)
    training_time = Column(DATETIME(fsp=6), nullable=False)
    dataset_list = Column(String(255), nullable=False)
    accuracy_rate = Column(Float(asdecimal=True), nullable=False)
    model_version = Column(String(255), nullable=False)
    model_fileaddr = Column(String(255), nullable=False)
    training_model_id = Column(INTEGER(11), nullable=False)


class ModelmanagementLabelinfo(Base):
    __tablename__ = 'modelmanagement_labelinfo'

    id = Column(INTEGER(11), primary_key=True)
    label_time = Column(DATETIME(fsp=6), nullable=False)
    label_name = Column(String(255), nullable=False)
    label_describe = Column(String(255), nullable=False)


class ModelmanagementPartinfo(Base):
    __tablename__ = 'modelmanagement_partinfo'

    id = Column(INTEGER(11), primary_key=True)
    part_name = Column(String(255), nullable=False)


class ModelmanagementReleaselabelindex(Base):
    __tablename__ = 'modelmanagement_releaselabelindex'

    id = Column(INTEGER(11), primary_key=True)
    F1score = Column(Float(asdecimal=True), nullable=False)
    Gscore = Column(Float(asdecimal=True), nullable=False)
    precision_rate = Column(Float(asdecimal=True), nullable=False)
    recall_rate = Column(Float(asdecimal=True), nullable=False)
    label_id = Column(INTEGER(11), nullable=False)
    release_model_id = Column(INTEGER(11), nullable=False)


class ModelmanagementReleasemodel(Base):
    __tablename__ = 'modelmanagement_releasemodel'

    id = Column(INTEGER(11), primary_key=True)
    model_name = Column(String(255), nullable=False)
    model_time = Column(DATETIME(fsp=6), nullable=False)
    model_part = Column(String(255), nullable=False)
    model_fileaddr = Column(String(255), nullable=False)
    accuracy_rate = Column(Float(asdecimal=True), nullable=False)
    model_describe = Column(String(255), nullable=False)
    user_id = Column(INTEGER(11), nullable=False)
    user_name = Column(String(255), nullable=False)
    model_id = Column(INTEGER(11), nullable=False)


class ModelmanagementTestlabelerror(Base):
    __tablename__ = 'modelmanagement_testlabelerror'

    id = Column(INTEGER(11), primary_key=True)
    pic_address = Column(String(255), nullable=False)
    old_label = Column(String(255), nullable=False)
    new_label = Column(String(255), nullable=False)
    testinfo_id = Column(INTEGER(11), nullable=False)


class ModelmanagementTestlabelindex(Base):
    __tablename__ = 'modelmanagement_testlabelindex'

    id = Column(INTEGER(11), primary_key=True)
    F1score = Column(Float(asdecimal=True), nullable=False)
    Gscore = Column(Float(asdecimal=True), nullable=False)
    precision_rate = Column(Float(asdecimal=True), nullable=False)
    recall_rate = Column(Float(asdecimal=True), nullable=False)
    label_id = Column(INTEGER(11), nullable=False)
    testinfo_id = Column(INTEGER(11), nullable=False)


class ModelmanagementTraininglabelindex(Base):
    __tablename__ = 'modelmanagement_traininglabelindex'

    id = Column(INTEGER(11), primary_key=True)
    F1score = Column(Float(asdecimal=True), nullable=False)
    Gscore = Column(Float(asdecimal=True), nullable=False)
    precision_rate = Column(Float(asdecimal=True), nullable=False)
    recall_rate = Column(Float(asdecimal=True), nullable=False)
    label_id = Column(INTEGER(11), nullable=False)
    traininginfo_id = Column(INTEGER(11), nullable=False)


class ModelmanagementTrainingmodelinfo(Base):
    __tablename__ = 'modelmanagement_trainingmodelinfo'

    id = Column(INTEGER(11), primary_key=True)
    model_name = Column(String(255), nullable=False)
    model_time = Column(DATETIME(fsp=6), nullable=False)
    training_status = Column(INTEGER(11), nullable=False)
    model_status = Column(INTEGER(11), nullable=False)
    release_version = Column(String(255))
    accuracy_rate = Column(Float(asdecimal=True))
    model_describe = Column(String(255), nullable=False)
    user_id = Column(INTEGER(11), nullable=False)
    user_name = Column(String(255), nullable=False)
    model_part_id = Column(INTEGER(11), nullable=False)


class Oauth2ProviderAccesstoken(Base):
    __tablename__ = 'oauth2_provider_accesstoken'

    id = Column(BIGINT(20), primary_key=True)
    token = Column(String(255), nullable=False)
    expires = Column(DATETIME(fsp=6), nullable=False)
    scope = Column(LONGTEXT, nullable=False)
    application_id = Column(BIGINT(20))
    user_id = Column(INTEGER(11))
    created = Column(DATETIME(fsp=6), nullable=False)
    updated = Column(DATETIME(fsp=6), nullable=False)
    source_refresh_token_id = Column(BIGINT(20))


class Oauth2ProviderApplication(Base):
    __tablename__ = 'oauth2_provider_application'

    id = Column(BIGINT(20), primary_key=True)
    client_id = Column(String(100), nullable=False)
    redirect_uris = Column(LONGTEXT, nullable=False)
    client_type = Column(String(32), nullable=False)
    authorization_grant_type = Column(String(32), nullable=False)
    client_secret = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    user_id = Column(INTEGER(11))
    skip_authorization = Column(TINYINT(1), nullable=False)
    created = Column(DATETIME(fsp=6), nullable=False)
    updated = Column(DATETIME(fsp=6), nullable=False)


class Oauth2ProviderGrant(Base):
    __tablename__ = 'oauth2_provider_grant'

    id = Column(BIGINT(20), primary_key=True)
    code = Column(String(255), nullable=False)
    expires = Column(DATETIME(fsp=6), nullable=False)
    redirect_uri = Column(String(255), nullable=False)
    scope = Column(LONGTEXT, nullable=False)
    application_id = Column(BIGINT(20), nullable=False)
    user_id = Column(INTEGER(11), nullable=False)
    created = Column(DATETIME(fsp=6), nullable=False)
    updated = Column(DATETIME(fsp=6), nullable=False)
    code_challenge = Column(String(128), nullable=False)
    code_challenge_method = Column(String(10), nullable=False)


class Oauth2ProviderRefreshtoken(Base):
    __tablename__ = 'oauth2_provider_refreshtoken'

    id = Column(BIGINT(20), primary_key=True)
    token = Column(String(255), nullable=False)
    access_token_id = Column(BIGINT(20))
    application_id = Column(BIGINT(20), nullable=False)
    user_id = Column(INTEGER(11), nullable=False)
    created = Column(DATETIME(fsp=6), nullable=False)
    updated = Column(DATETIME(fsp=6), nullable=False)
    revoked = Column(DATETIME(fsp=6))


class OperatorsOperatorcategory(Base):
    __tablename__ = 'operators_operatorcategory'

    id = Column(INTEGER(11), primary_key=True)
    category_name = Column(String(255), nullable=False)
    category_describe = Column(String(255), nullable=False)


class OperatorsOperatorinfo(Base):
    __tablename__ = 'operators_operatorinfo'

    id = Column(INTEGER(11), primary_key=True)
    operator_name = Column(String(255), nullable=False)
    operator_time = Column(DATETIME(fsp=6), nullable=False)
    operator_type = Column(INTEGER(11), nullable=False)
    operator_url = Column(String(255))
    operator_describe = Column(String(255), nullable=False)
    operator_category_id = Column(INTEGER(11), nullable=False)
