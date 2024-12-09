<script setup>
import SubstitutionCard from "./SubstitutionCard.vue";
import SubstitutionLoader from "./SubstitutionLoader.vue";
import InfiniteScrollingDateSortedCRUDIterator from "aleksis.core/components/generic/InfiniteScrollingDateSortedCRUDIterator.vue";

import {
  amendedLessonsFromAbsences,
  createOrUpdateSubstitutions,
  deleteAmendLessons,
  gqlGroups,
  gqlRooms,
  gqlSubjects,
  gqlTeachers,
} from "../amendLesson.graphql";

import { DateTime } from "luxon";
</script>

<template>
  <infinite-scrolling-date-sorted-c-r-u-d-iterator
    :gql-query="gqlQuery"
    :gql-additional-query-args="gqlQueryArgs"
    :gql-patch-mutation="gqlPatchMutation"
    :get-patch-data="gqlGetPatchData"
    i18n-key="chronos.substitutions.overview"
    :enable-search="true"
    :enable-create="false"
    :show-create="false"
    :enable-delete="false"
    :enable-edit="true"
    :elevated="false"
    :force-model-item-update="true"
    :day-increment="3"
    empty-icon="mdi-account-multiple-check-outline"
    ref="iterator"
  >
    <template #additionalActions="{ attrs, on }">
      <v-autocomplete
        :items="groups"
        item-text="name"
        item-value="id"
        clearable
        filled
        dense
        hide-details
        :placeholder="$t('chronos.substitutions.overview.filter.groups')"
        :loading="$apollo.queries.groups.loading"
        :value="objId"
        @input="changeGroup"
        @click:clear="changeGroup"
      />
      <v-autocomplete
        :items="amendableTeachers"
        item-text="fullName"
        item-value="id"
        clearable
        filled
        dense
        hide-details
        :placeholder="$t('chronos.substitutions.overview.filter.teachers')"
        :loading="$apollo.queries.amendableTeachers.loading"
        :value="teacherId"
        @input="changeTeacher"
        @click:clear="changeTeacher"
      />
      <v-switch
        :loading="$apollo.queries.groups.loading"
        :label="$t('chronos.substitutions.overview.filter.missing')"
        v-model="incomplete"
        dense
        inset
        hide-details
        class="ml-6"
      />

      <v-alert type="info" outlined dense class="full-width">
        <v-row align="center" no-gutters>
          <v-col cols="12" md="9">
            {{ $t("chronos.substitutions.overview.info_alert.text") }}
          </v-col>
          <v-col cols="12" md="3" align="right">
            <v-btn
              color="info"
              outlined
              small
              :to="{ name: 'kolego.absences' }"
            >
              {{ $t("chronos.substitutions.overview.info_alert.button") }}
            </v-btn>
          </v-col>
        </v-row>
      </v-alert>
    </template>

    <template #item="{ item, lastQuery }">
      <substitution-card
        :substitution="item"
        :affected-query="lastQuery"
        :is-create="false"
        :gql-patch-mutation="gqlPatchMutation"
        :gql-delete-mutation="gqlDeleteMutation"
        :amendable-rooms="amendableRooms"
        :amendable-subjects="amendableSubjects"
        :amendable-teachers="amendableTeachers"
        @delete="handleDelete"
      />
    </template>

    <template #itemLoader>
      <substitution-loader />
    </template>
  </infinite-scrolling-date-sorted-c-r-u-d-iterator>
</template>

<script>
export default {
  name: "SubstitutionOverview",
  props: {
    objId: {
      type: [Number, String],
      required: false,
      default: null,
    },
    teacherId: {
      type: [Number, String],
      required: false,
      default: null,
    },
  },
  data() {
    return {
      gqlQuery: amendedLessonsFromAbsences,
      gqlPatchMutation: createOrUpdateSubstitutions,
      gqlDeleteMutation: deleteAmendLessons,
      groups: [],
      amendableTeachers: [],
      incomplete: false,
    };
  },
  methods: {
    gqlGetPatchData(item) {
      return { id: item.id, teachers: item.teachers };
    },
    changeGroup(group) {
      this.$router.push({
        name: "chronos.substitutionOverview",
        params: {
          objId: group ? group : "all",
          teacherId: this.teacherId,
        },
        hash: this.$route.hash,
      });
      this.$refs.iterator.resetDate();
    },
    changeTeacher(teacher) {
      this.$router.push({
        name: "chronos.substitutionOverview",
        params: {
          teacherId: teacher ? teacher : "all",
          objId: this.objId,
        },
        hash: this.$route.hash,
      });
      this.$refs.iterator.resetDate();
    },
    handleDelete(datetime) {
      this.$refs.iterator.refetchDay(DateTime.fromISO(datetime).toISODate());
    },
  },
  computed: {
    gqlQueryArgs() {
      return {
        objId: this.objId === "all" ? null : Number(this.objId),
        teacher: this.teacherId === "all" ? null : Number(this.teacherId),
        incomplete: !!this.incomplete,
      };
    },
  },
  apollo: {
    groups: gqlGroups,
    amendableRooms: gqlRooms,
    amendableSubjects: gqlSubjects,
    amendableTeachers: gqlTeachers,
  },
};
</script>
