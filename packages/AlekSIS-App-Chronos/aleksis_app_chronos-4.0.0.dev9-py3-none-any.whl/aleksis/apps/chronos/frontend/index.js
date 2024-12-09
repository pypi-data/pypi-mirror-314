import { hasPersonValidator } from "aleksis.core/routeValidators";

import Substitutions from "./components/Substitutions.vue";
import { DateTime } from "luxon";

export default {
  meta: {
    inMenu: true,
    titleKey: "chronos.menu_title",
    icon: "mdi-school-outline",
    iconActive: "mdi-school",
    permission: "chronos.view_menu_rule",
  },
  children: [
    {
      path: "timetable/",
      component: () => import("./components/Timetable.vue"),
      name: "chronos.timetable",
      meta: {
        inMenu: true,
        titleKey: "chronos.timetable.menu_title",
        toolbarTitle: "chronos.timetable.menu_title",
        icon: "mdi-grid",
        permission: "chronos.view_timetable_overview_rule",
        fullWidth: true,
      },
    },
    {
      path: "timetable/:type/:id/",
      component: () => import("./components/Timetable.vue"),
      name: "chronos.timetableWithId",
      meta: {
        permission: "chronos.view_timetable_overview_rule",
        fullWidth: true,
      },
      children: [
        {
          path: ":view(month|week|day)/:year(\\d\\d\\d\\d)/:month(\\d\\d)/:day(\\d\\d)/",
          component: () => import("./components/Timetable.vue"),
          name: "chronos.timetableWithIdAndParams",
          meta: {
            permission: "chronos.view_timetable_overview_rule",
            fullWidth: true,
          },
        },
      ],
    },
    {
      path: "substitution_overview/",
      component: () =>
        import("./components/substitutions/SubstitutionOverview.vue"),
      redirect: () => {
        return {
          path: "substitution_overview/group/all/person/all/",
          hash: "#" + DateTime.now().toISODate(),
        };
      },
      name: "chronos.substitutionOverviewLanding",
      props: true,
      meta: {
        inMenu: true,
        icon: "mdi-account-convert-outline",
        iconActive: "mdi-account-convert",
        titleKey: "chronos.substitutions.overview.menu_title",
        toolbarTitle: "chronos.substitutions.overview.menu_title",
        permission: "chronos.view_substitution_overview_rule",
      },
      children: [
        {
          path: "group/:objId(all|\\d+)?/person/:teacherId(all|\\d+)?/",
          component: () =>
            import("./components/substitutions/SubstitutionOverview.vue"),
          name: "chronos.substitutionOverview",
          meta: {
            titleKey: "chronos.substitutions.overview.menu_title",
            toolbarTitle: "chronos.substitutions.overview.menu_title",
            permission: "chronos.view_substitution_overview_rule",
            fullWidth: true,
          },
        },
      ],
    },
    {
      path: "substitutions/print/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "chronos.printSubstitutions",
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
    },
    {
      path: "substitutions/print/:date/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "chronos.printSubstitutionsForDate",
      props: {
        byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
      },
    },
    {
      path: "substitutions/",
      props: true,
      component: Substitutions,
      name: "chronos.listSubstitutionsForDateLanding",
      redirect: () => {
        return {
          name: "chronos.listSubstitutionsForDate",
          params: {
            date: DateTime.now().toISODate(),
          },
        };
      },
      meta: {
        inMenu: true,
        titleKey: "chronos.substitutions.menu_title",
        toolbarTitle: "chronos.substitutions.menu_title",
        icon: "mdi-list-status",
        permission: "chronos.view_substitutions_rule",
      },
      children: [
        {
          path: ":date/",
          component: Substitutions,
          name: "chronos.listSubstitutionsForDate",
          meta: {
            toolbarTitle: "chronos.substitutions.menu_title",
            permission: "chronos.view_substitutions_rule",
          },
        },
      ],
    },
  ],
};
