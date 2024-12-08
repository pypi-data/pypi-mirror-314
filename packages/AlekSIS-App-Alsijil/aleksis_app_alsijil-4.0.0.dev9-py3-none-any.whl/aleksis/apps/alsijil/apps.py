from aleksis.core.util.apps import AppConfig


class AlsijilConfig(AppConfig):
    name = "aleksis.apps.alsijil"
    verbose_name = "AlekSIS — Alsijil (Class register)"

    urls = {
        "Repository": "https://edugit.org/AlekSIS/official/AlekSIS-App-Alsijil/",
    }
    licence = "EUPL-1.2+"
    copyright_info = (
        ([2019, 2021], "Dominik George", "dominik.george@teckids.org"),
        ([2019, 2020], "Tom Teichler", "tom.teichler@teckids.org"),
        ([2019], "mirabilos", "thorsten.glaser@teckids.org"),
        ([2020, 2021, 2022, 2024], "Jonathan Weth", "dev@jonathanweth.de"),
        ([2020, 2021, 2024], "Julian Leucker", "leuckeju@katharineum.de"),
        ([2020, 2022, 2023, 2024], "Hangzhi Yu", "yuha@katharineum.de"),
        ([2021], "Lloyd Meins", "meinsll@katharineum.de"),
        ([2024], "Michael Bauer", "michael-bauer@posteo.de"),
    )

    def post_migrate(
        self,
        app_config: AppConfig,
        verbosity: int,
        interactive: bool,
        using: str,
        **kwargs,
    ) -> None:
        super().post_migrate(app_config, verbosity, interactive, using, **kwargs)
        from .util.alsijil_helpers import get_absence_reason_tag

        get_absence_reason_tag()
