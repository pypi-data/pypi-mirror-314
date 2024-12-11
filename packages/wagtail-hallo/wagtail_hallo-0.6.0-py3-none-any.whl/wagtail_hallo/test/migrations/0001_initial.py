from django.db import migrations, models
import django.db.models.deletion

from wagtail import blocks, fields


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("wagtailcore", "0062_comment_models_and_pagesubscription"),
    ]

    operations = [
        migrations.CreateModel(
            name="HalloTestPage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
                    ),
                ),
                ("body", fields.RichTextField(blank=True)),
                (
                    "body_stream",
                    fields.StreamField(
                        [
                            (
                                "heading",
                                blocks.CharBlock(form_classname="full title"),
                            ),
                            (
                                "paragraph",
                                blocks.RichTextBlock(editor="hallo"),
                            ),
                        ],
                        use_json_field=True,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("wagtailcore.page",),
        ),
    ]
