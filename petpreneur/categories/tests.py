import django.core
import django.test
import django.urls
import parameterized

import categories.forms
import categories.models


class ModelsTests(django.test.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.skill = categories.models.Skill.objects.create(
            name="Тестовый скилл",
            slug="test-skill-slug",
        )

    @parameterized.parameterized.expand(
        [
            ("Тестовый скилл!"),
            ("тестовыйскилл"),
            ("тесто вый .---скилл!%:"),
        ],
    )
    def test_create_skill_with_invalid_name(self, skill_name):
        skill_count = categories.models.Skill.objects.count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.skill = categories.models.Skill(
                name=skill_name,
                slug="sluuuug",
            )
            self.skill.full_clean()
            self.skill.save()
        self.assertEqual(categories.models.Skill.objects.count(), skill_count)

    @parameterized.parameterized.expand(
        [
            ("Тестовый скилл1!"),
            ("тестовыйскилл2"),
            ("тесто вый .---скилл3!%:"),
        ],
    )
    def test_create_skill_with_valid_name(self, skill_name):
        skill_count = categories.models.Skill.objects.count()
        self.skill = categories.models.Skill(
            name=skill_name,
            slug="sluuuug",
        )
        self.skill.full_clean()
        self.skill.save()
        self.assertEqual(
            categories.models.Skill.objects.count(),
            skill_count + 1,
        )


class FormTests(django.test.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.form = categories.forms.SkillChangeForm()

    def test_labels(self):
        label = FormTests.form.fields["name"].label
        self.assertEqual(label, "Навыки")

    def test_create_valid_form(self):
        form_data = {
            "name": "banana",
        }

        response = django.test.Client().post(
            django.urls.reverse("users:resumes"),
            data=form_data,
            follow=True,
        )

        self.assertIn("form", response.context)


__all__ = []
