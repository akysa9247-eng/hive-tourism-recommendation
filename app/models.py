from django.db import models

class AdsSightHeatScoreRate(models.Model):
    dt = models.DateField(primary_key=True)
    province = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    sight_count = models.IntegerField(blank=True, null=True)
    heat_score_9_to_10 = models.IntegerField(blank=True, null=True)
    heat_score_8_to_9 = models.IntegerField(blank=True, null=True)
    heat_score_7_to_8 = models.IntegerField(blank=True, null=True)
    heat_score_6_to_7 = models.IntegerField(blank=True, null=True)
    heat_score_0_to_6 = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ads_sight_heat_score_rate'
        unique_together = (('dt', 'province', 'city'),)


class AdsSightScoreRate(models.Model):
    dt = models.DateField(primary_key=True)
    province = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    sight_count = models.IntegerField(blank=True, null=True)
    score_count_4_5_to_5 = models.IntegerField(blank=True, null=True)
    score_count_4_to_4_5 = models.IntegerField(blank=True, null=True)
    score_count_3_5_to_4 = models.IntegerField(blank=True, null=True)
    score_count_3_to_3_5 = models.IntegerField(blank=True, null=True)
    score_count_0_to_3 = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ads_sight_score_rate'
        unique_together = (('dt', 'province', 'city'),)


class AdsCityStats(models.Model):
    dt = models.DateField(primary_key=True)
    province = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    heat_score = models.IntegerField(blank=True, null=True)
    sight_count = models.IntegerField(blank=True, null=True)
    sight_count_5a = models.IntegerField(blank=True, null=True)
    sight_count_4a = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ads_city_stats'
        unique_together = (('dt', 'province', 'city'),)


class AdsProvinceStats(models.Model):
    dt = models.DateField(primary_key=True)
    province = models.CharField(max_length=255)
    heat_score = models.IntegerField(blank=True, null=True)
    sight_count = models.IntegerField(blank=True, null=True)
    sight_count_5a = models.IntegerField(blank=True, null=True)
    sight_count_4a = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ads_province_stats'
        unique_together = (('dt', 'province'),)

class AdsSightHeatScoreTop10Stats(models.Model):
    dt = models.DateField(primary_key=True)
    sight_id = models.IntegerField()
    sight_name = models.CharField(max_length=255, blank=True, null=True)
    province = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    tag_list = models.CharField(max_length=2555, blank=True, null=True)
    level = models.CharField(max_length=255, blank=True, null=True)
    heat_score = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    score = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    telephone = models.CharField(max_length=255, blank=True, null=True)
    intro = models.CharField(max_length=255, blank=True, null=True)
    opening_time = models.CharField(max_length=255, blank=True, null=True)
    img_list = models.TextField(blank=True, null=True)
    cover = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ads_sight_heat_score_top_10_stats'
        unique_together = (('dt', 'sight_id'),)


class AdsCommentSightScoreRate(models.Model):
    dt = models.DateField(primary_key=True)
    province = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    score_count = models.IntegerField(blank=True, null=True)
    comment_score_count_5 = models.IntegerField(blank=True, null=True)
    comment_score_count_4 = models.IntegerField(blank=True, null=True)
    comment_score_count_3 = models.IntegerField(blank=True, null=True)
    comment_score_count_2 = models.IntegerField(blank=True, null=True)
    comment_score_count_1 = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ads_comment_sight_score_rate'


class AdsSightCountStats(models.Model):
    dt = models.DateField(primary_key=True)
    total_sight_count = models.IntegerField(blank=True, null=True)
    total_sight_count_5a = models.IntegerField(blank=True, null=True)
    total_sight_count_4a = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ads_sight_count_stats'


class AdsSightProvinceStats(models.Model):
    dt = models.DateField(primary_key=True)
    province = models.CharField(max_length=255)
    heat_score = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    sight_count = models.IntegerField(blank=True, null=True)
    sight_count_5a = models.IntegerField(blank=True, null=True)
    sight_count_4a = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ads_sight_province_stats'
        unique_together = (('dt', 'province'),)

class AdsSightScoreTop10Stats(models.Model):
    dt = models.DateField(primary_key=True)
    sight_id = models.IntegerField()
    sight_name = models.CharField(max_length=255, blank=True, null=True)
    province = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    tag_list = models.CharField(max_length=2555, blank=True, null=True)
    level = models.CharField(max_length=255, blank=True, null=True)
    heat_score = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    score = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    telephone = models.CharField(max_length=255, blank=True, null=True)
    intro = models.TextField(blank=True, null=True)
    opening_time = models.CharField(max_length=255, blank=True, null=True)
    img_list = models.CharField(max_length=255, blank=True, null=True)
    cover = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ads_sight_score_top_10_stats'
        unique_together = (('dt', 'sight_id'),)


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)

class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'

class SightInfo(models.Model):
    sight_id = models.IntegerField(primary_key=True)
    sight_name = models.CharField(max_length=255, blank=True, null=True)
    province = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    tag_list = models.CharField(max_length=2555, blank=True, null=True)
    level = models.CharField(max_length=255, blank=True, null=True)
    heat_score = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    score = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    telephone = models.CharField(max_length=255, blank=True, null=True)
    intro = models.TextField(blank=True, null=True)
    opening_time = models.CharField(max_length=2555, blank=True, null=True)
    img_list = models.CharField(max_length=2555, blank=True, null=True)
    cover = models.CharField(max_length=2555, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sight_info'

class CommentInfo(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    sight_id = models.IntegerField()
    content = models.TextField()
    score = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'comment_info'

class UserInfo(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=255)
    password = models.CharField(max_length=255)
    contact_info = models.CharField(max_length=255)
    sex = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatar/', default='avatar/default.jpg')
    intro = models.CharField(max_length=255, blank=True, null=True)
    last_login_time = models.DateTimeField()
    create_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'user_info'

class AdminInfo(models.Model):
    adminname = models.CharField(unique=True, max_length=255)
    password = models.CharField(max_length=255)
    contact_info = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to='avatar/', default='avatar/default.jpg')
    intro = models.CharField(max_length=255, blank=True, null=True)
    last_login_time = models.DateTimeField()
    create_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'admin_info'

class UserFavorites(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    sight_id = models.IntegerField()
    favorited_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'user_favorites'

class UserBrowses(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    sight_id = models.IntegerField()
    browse_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'user_browses'

class UserSearchRecords(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    search_value = models.CharField(max_length=255)
    search_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'user_search_records'

class SpiderCommentInfo(models.Model):
    username = models.CharField(max_length=255)
    sight_id = models.IntegerField()
    content = models.TextField()
    score = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    class Meta:
        managed = False
        db_table = 'spider_comment_info'

class ProvinceCity(models.Model):
    province = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    city_link = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'province_city'

class CommentInfoTest(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    sight_id = models.IntegerField()
    content = models.TextField()
    score = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'comment_info_test'

class UserInfoTest(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=255)
    password = models.CharField(max_length=255)
    contact_info = models.CharField(max_length=255)
    sex = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatar/', default='avatar/default.jpg')
    intro = models.CharField(max_length=255, blank=True, null=True)
    last_login_time = models.DateTimeField()
    create_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'user_info_test'


class UserFavoritesTest(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    sight_id = models.IntegerField()
    favorited_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'user_favorites_test'

class UserBrowsesTest(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    sight_id = models.IntegerField()
    browse_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'user_browses_test'

class UserRecommendationValues(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    sight_id = models.IntegerField()
    recommendation_value = models.FloatField()

    class Meta:
        managed = False
        db_table = 'user_recommendation_values'

class UserRecommendationValuesTest(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    sight_id = models.IntegerField()
    recommendation_value = models.FloatField()

    class Meta:
        managed = False
        db_table = 'user_recommendation_values_test'

class UserRecommendationValuesWithPenaltyTest(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    sight_id = models.IntegerField()
    recommendation_value = models.FloatField()

    class Meta:
        managed = False
        db_table = 'user_recommendation_values_with_penalty_test'