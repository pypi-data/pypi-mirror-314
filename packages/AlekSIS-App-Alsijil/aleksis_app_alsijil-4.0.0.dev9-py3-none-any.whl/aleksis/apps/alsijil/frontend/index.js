import { hasPersonValidator } from "aleksis.core/routeValidators";
import { DateTime } from "luxon";
import { MODE } from "./components/coursebook/statistics/modes";

export const collectionItems = {
  coreGroupActions: [
    {
      key: "alsijil-open-coursebook",
      component: () =>
        import("./components/injectables/group_actions/OpenCoursebook.vue"),
      isActive: () => true,
    },
    {
      key: "alsijil-show-absences",
      component: () =>
        import("./components/injectables/group_actions/ShowAbsences.vue"),
      isActive: () => true,
    },
  ],
  coreGroupOverview: [
    {
      tab: {
        id: "alsijil.statistics",
        titleKey: "group.tabs.statistics_tab",
      },
      titleKey: "group.tabs.statistics",
      component: () =>
        import("./components/coursebook/statistics/StatisticsForGroupTab.vue"),
    },
  ],
  corePersonWidgets: [
    {
      key: "core-person-widgets",
      component: () =>
        import(
          "./components/coursebook/statistics/StatisticsForPersonCard.vue"
        ),
      shouldDisplay: () => true,
      colProps: {
        cols: 12,
        md: 6,
        lg: 4,
      },
    },
  ],
};

export default {
  meta: {
    inMenu: true,
    titleKey: "alsijil.menu_title",
    icon: "mdi-account-group-outline",
    iconActive: "mdi-account-group",
    permission: "alsijil.view_menu_rule",
  },
  props: {
    byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
  },
  children: [
    {
      path: "coursebook/",
      component: () => import("./components/coursebook/Coursebook.vue"),
      redirect: () => {
        return {
          name: "alsijil.coursebook",
          params: {
            filterType: "my",
            pageType: "documentations",
          },
          hash: "#" + DateTime.now().toISODate(),
        };
      },
      name: "alsijil.coursebook_landing",
      props: true,
      meta: {
        inMenu: true,
        icon: "mdi-book-education-outline",
        iconActive: "mdi-book-education",
        titleKey: "alsijil.coursebook.menu_title",
        toolbarTitle: "alsijil.coursebook.menu_title",
        permission: "alsijil.view_documentations_menu_rule",
      },
      children: [
        {
          path: ":pageType(documentations|absences)/:filterType(my|all)/:objType(group|course|teacher)?/:objId(\\d+)?/",
          component: () => import("./components/coursebook/Coursebook.vue"),
          name: "alsijil.coursebook",
          meta: {
            titleKey: "alsijil.coursebook.menu_title",
            toolbarTitle: "alsijil.coursebook.menu_title",
            permission: "alsijil.view_documentations_menu_rule",
            fullWidth: true,
          },
        },
      ],
    },
    {
      path: "print/groups/:groupIds+/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "alsijil.coursebook_print",
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
    },
    {
      path: "extra_marks/",
      component: () => import("./components/extra_marks/ExtraMarks.vue"),
      name: "alsijil.extraMarks",
      meta: {
        inMenu: true,
        titleKey: "alsijil.extra_marks.menu_title",
        icon: "mdi-label-variant-outline",
        iconActive: "mdi-label-variant",
        permission: "alsijil.view_extramarks_rule",
      },
    },
    {
      path: `statistics/:personId/:mode(${Object.values(MODE).join("|")})`,
      component: () =>
        import(
          "./components/coursebook/statistics/StatisticsForPersonPage.vue"
        ),
      name: "alsijil.coursebook_statistics",
      props: true,
      meta: {
        inMenu: false,
        titleKey: "alsijil.coursebook.statistics.person_compact.title",
        toolbarTitle: "alsijil.coursebook.statistics.person_compact.title",
        // TODO: Add permission & change it here.
        permission: "alsijil.view_documentations_menu_rule",
      },
    },
  ],
};
