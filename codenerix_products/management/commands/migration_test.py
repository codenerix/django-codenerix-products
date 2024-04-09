from django.core.management.base import BaseCommand

from codenerix_lib.debugger import Debugger
from django.conf import settings

from django.db import connection, transaction

from codenerix_products.models import (
    MODELS,
    GroupValueAttribute,
    Attribute,
    OptionValueAttribute,
    GroupValueFeature,
    Feature,
    OptionValueFeature,
    GroupValueFeatureSpecial,
    FeatureSpecial,
    OptionValueFeatureSpecial,
)

for info in MODELS:
    field = info[0]
    model = info[1]
    for lang_code in settings.LANGUAGES_DATABASES:
        cad = "from codenerix_products.models import {}Text{}\n".format(
            model, lang_code
        )
        exec(cad)


class Command(BaseCommand, Debugger):
    def migrate(self, model_group, table_source, model_option):
        model_str = (
            str(model_option)
            .replace('"', "")
            .replace("'", "")
            .replace(">", "")
            .split(".")[-1]
        )

        cursor = connection.cursor()
        query = """
            SELECT cpa.id, cpa.list_value_id, cpg.name
            FROM {table} AS cpa, codenerix_products_groupvalue AS cpg
            WHERE cpa.list_value_id = cpg.id
        """.format(
            **{"table": table_source}
        )
        cursor.execute(query)
        for src in cursor:
            if src[1]:
                group_id = src[1]
                group_name = src[2]

                group = model_group.objects.filter(name=group_name).first()
                if not group:
                    group = model_group()
                    group.name = group_name
                    group.save()

                text_lang = []
                froms = [
                    "codenerix_products_optionvalue cpo",
                ]
                conditions = [
                    "cpo.group_id = {}".format(group_id),
                ]
                values = []

                for lang_code in settings.LANGUAGES_DATABASES:
                    model_lang = globals()[
                        "{}Text{}".format(model_str, lang_code)
                    ]
                    text_lang.append(
                        (lang_code, model_lang._meta.db_table, model_lang)
                    )

                    alias = "t{}".format(lang_code.lower())
                    values.append("{}.description".format(alias))
                    froms.append(
                        "codenerix_products_optionvaluetext{lang} {alias}".format(
                            **{"lang": lang_code.lower(), "alias": alias}
                        )
                    )
                    conditions.append(
                        "{}.option_value_id = cpo.id".format(alias)
                    )

                query_text = "SELECT {} FROM {} WHERE {}".format(
                    ",".join(values), ",".join(froms), " AND ".join(conditions)
                )

                froms = [
                    "codenerix_products_optionvalue cpo",
                ]
                conditions = [
                    "cpo.group_id = {}".format(group_id),
                ]
                for tl in text_lang:
                    alias = "t{}".format(tl[0].lower())
                    table = tl[1]

                    froms.append("{} {}".format(table, alias))
                    conditions.append(
                        "{}.option_value_id = cpo.id".format(alias)
                    )

                cursor.execute(query_text)

                for option in cursor:
                    cond_extra = []
                    for v, o in zip(values, option):
                        a = '{} = "{}"'.format(v, o)
                        cond_extra.append(a)

                    q_option = (
                        "SELECT COUNT(*) FROM {} WHERE {} AND {}".format(
                            ",".join(froms),
                            " AND ".join(conditions),
                            " AND ".join(cond_extra),
                        )
                    )

                    cursor.execute(q_option)
                    count = cursor.fetchone()

                    if count[0] == 0:
                        opt = model_option()
                        opt.group = group
                        opt.save()

                        for info_lang, description in zip(text_lang, option):
                            model_lang = info_lang[2]
                            opt_lang = model_lang()
                            opt_lang.description = description
                            opt_lang.option_value = opt
                            opt_lang.save()

        return 0

    def handle(self, *args, **options):

        self.migrate(
            GroupValueAttribute,
            "codenerix_products_attribute",
            OptionValueAttribute,
        )
        self.migrate(
            GroupValueFeature, "codenerix_products_feature", OptionValueFeature
        )
        self.migrate(
            GroupValueFeatureSpecial,
            "codenerix_products_featurespecial",
            OptionValueFeatureSpecial,
        )
