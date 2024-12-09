<script setup>
import CRUDList from "aleksis.core/components/generic/CRUDList.vue";
import PrimaryActionButton from "aleksis.core/components/generic/buttons/PrimaryActionButton.vue";
import PersonChip from "aleksis.core/components/person/PersonChip.vue";
import GroupChip from "aleksis.core/components/group/GroupChip.vue";
import DateSelectFooter from "aleksis.core/components/generic/DateSelectFooter.vue";
</script>

<template>
  <c-r-u-d-list
    :gql-query="query"
    :gql-additional-query-args="{ date: date }"
    :get-gql-data="prepareList"
    :headers="headers"
    :disable-sort="true"
    :item-class="itemColor"
    :show-select="false"
    :enable-create="false"
    :enable-edit="false"
    :dense="true"
    :items-per-page="-1"
    :mobile-breakpoint="0"
  >
    <template #title>
      <v-card-title class="full-width flex-nowrap pb-0">
        {{
          $d(
            new Date(date),
            $vuetify.breakpoint.xs ? "shortWithWeekday" : "dateWithWeekday",
          )
        }}
        <v-spacer />
        <primary-action-button
          i18n-key="chronos.substitutions.print"
          icon-text="$print"
          :icon="$vuetify.breakpoint.xs"
          :to="{
            name: 'chronos.printSubstitutionsForDate',
            params: {
              date: date,
            },
          }"
        />
      </v-card-title>

      <v-card-text
        v-if="affectedTeachers.length > 0 || affectedGroups.length > 0"
        class="pb-0"
      >
        <v-expansion-panels accordion multiple flat>
          <v-expansion-panel v-if="affectedTeachers.length > 0">
            <v-expansion-panel-header class="px-0">
              <strong>{{
                $t("chronos.substitutions.affected_teachers")
              }}</strong>
            </v-expansion-panel-header>
            <v-expansion-panel-content>
              <person-chip
                v-for="teacher in affectedTeachers"
                :key="teacher.id"
                class="ma-1"
                :person="teacher"
                small
                :to="{
                  name: 'chronos.timetableWithId',
                  params: {
                    type: 'person',
                    id: teacher.id,
                  },
                }"
              />
            </v-expansion-panel-content>
          </v-expansion-panel>

          <v-expansion-panel v-if="affectedGroups.length > 0">
            <v-expansion-panel-header class="px-0">
              <strong>
                {{ $t("chronos.substitutions.affected_groups") }}</strong
              >
            </v-expansion-panel-header>
            <!-- TODO: Link to group-timetable as well -->
            <!-- as soon as it becomes possible to resolve a -->
            <!-- group-timetable from the lesson-event group too. -->
            <v-expansion-panel-content class="px-0">
              <group-chip
                v-for="group in affectedGroups"
                class="ma-1"
                :key="group.id"
                :group="group"
                format="short"
                small
              />
            </v-expansion-panel-content>
          </v-expansion-panel>
        </v-expansion-panels>
      </v-card-text>
    </template>
    <!-- TODO: Extract strike -> bold || normal pattern into own -->
    <!-- component and reuse? -->
    <template #groups="{ item: { oldGroups, newGroups } }">
      <span v-if="newGroups.length > 0">
        <span class="strike-through">
          <lesson-event-link-iterator
            :items="oldGroups"
            attr="shortName"
            alternative-attr="name"
          />
        </span>
        <!-- eslint-disable-next-line @intlify/vue-i18n/no-raw-text -->
        <span>&nbsp;→&nbsp;</span>
        <strong>
          <lesson-event-link-iterator
            :items="newGroups"
            attr="shortName"
            alternative-attr="name"
          />
        </strong>
      </span>
      <span v-else>
        <lesson-event-link-iterator
          :items="oldGroups"
          attr="shortName"
          alternative-attr="name"
        />
      </span>
    </template>
    <template #time="{ item: { startSlot, endSlot, startTime, endTime } }">
      <span v-if="startSlot && endSlot && startSlot === endSlot">
        {{ startSlot }}.
      </span>
      <span v-else-if="startSlot && endSlot">
        {{ startSlot }}.–{{ endSlot }}.
      </span>
      <span v-else-if="startTime && endTime">
        {{ $d(new Date(startTime), "shortTime") }}
        –
        {{ $d(new Date(endTime), "shortTime") }}
      </span>
      <span v-else>{{ $t("chronos.substitutions.all_day") }}</span>
    </template>
    <template #teachers="{ item: { oldTeachers, newTeachers } }">
      <span v-if="newTeachers.length > 0">
        <span class="strike-through">
          <lesson-event-link-iterator
            :items="oldTeachers"
            attr="shortName"
            alternative-attr="fullName"
          />
        </span>
        <!-- eslint-disable-next-line @intlify/vue-i18n/no-raw-text -->
        <span>&nbsp;→&nbsp;</span>
        <strong>
          <lesson-event-link-iterator
            :items="newTeachers"
            attr="shortName"
            alternative-attr="fullName"
          />
        </strong>
      </span>
      <span v-else>
        <lesson-event-link-iterator
          :items="oldTeachers"
          attr="shortName"
          alternative-attr="fullName"
        />
      </span>
    </template>
    <template #subject="{ item: { oldSubject, newSubject } }">
      <span v-if="oldSubject === 'SUPERVISION'">
        {{ $t("chronos.substitutions.supervision") }}
      </span>
      <span v-else-if="newSubject">
        <span class="strike-through">{{ oldSubject }}</span>
        <!-- eslint-disable-next-line @intlify/vue-i18n/no-raw-text -->
        <span>&nbsp;→&nbsp;</span>
        <strong>{{ newSubject }}</strong>
      </span>
      <span v-else>{{ oldSubject }}</span>
    </template>
    <template #rooms="{ item: { oldRooms, newRooms } }">
      <span v-if="newRooms.length > 0">
        <span class="strike-through">
          <lesson-event-link-iterator
            :items="oldRooms"
            attr="shortName"
            alternative-attr="name"
          />
        </span>
        <!-- eslint-disable-next-line @intlify/vue-i18n/no-raw-text -->
        <span>&nbsp;→&nbsp;</span>
        <strong>
          <lesson-event-link-iterator
            :items="newRooms"
            attr="shortName"
            alternative-attr="name"
          />
        </strong>
      </span>
      <span v-else>
        <lesson-event-link-iterator
          :items="oldRooms"
          attr="shortName"
          alternative-attr="name"
        />
      </span>
    </template>
    <template #notes="{ item: { cancelled, notes } }">
      <v-chip v-if="cancelled" color="green" text-color="white" small>
        {{ $t("chronos.substitutions.cancelled") }}
      </v-chip>
      {{ notes }}
    </template>
    <template #no-data>
      {{ $t("chronos.substitutions.no_substitutions") }}
    </template>
    <template #footer>
      <!-- TODO: Skip over unneeded days; eg. weekends. -->
      <date-select-footer
        :value="date"
        @input="gotoDate"
        @prev="gotoDate(DateTime.fromISO(date).minus({ days: 1 }).toISODate())"
        @next="gotoDate(DateTime.fromISO(date).plus({ days: 1 }).toISODate())"
      />
    </template>
  </c-r-u-d-list>
</template>

<script>
import { substitutionsForDate } from "./substitutions.graphql";
import { DateTime } from "luxon";

import LessonEventLinkIterator from "./LessonEventLinkIterator.vue";

export default {
  name: "Substitutions",
  components: { LessonEventLinkIterator },
  props: {
    date: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      query: substitutionsForDate,
      affectedTeachers: [],
      affectedGroups: [],
      headers: [
        {
          text: this.$t("chronos.substitutions.groups"),
          value: "groups",
        },
        {
          text: this.$t("chronos.substitutions.time"),
          value: "time",
        },
        {
          text: this.$t("chronos.substitutions.teachers"),
          value: "teachers",
        },
        {
          text: this.$t("chronos.substitutions.subject"),
          value: "subject",
        },
        {
          text: this.$t("chronos.substitutions.rooms"),
          value: "rooms",
        },
        {
          text: this.$t("chronos.substitutions.notes"),
          value: "notes",
        },
      ],
    };
  },
  methods: {
    prepareList(data) {
      this.affectedTeachers = data.affectedTeachers;
      this.affectedGroups = data.affectedGroups;
      return data.substitutions;
    },
    itemColor(item) {
      return item.cancelled ? "green-text" : "";
    },
    gotoDate(date) {
      this.$router.push({
        name: "chronos.listSubstitutionsForDate",
        params: {
          date: date,
        },
      });
    },
  },
};
</script>

<style>
.green-text {
  color: green;
}
.strike-through {
  text-decoration: line-through;
}
.v-expansion-panel-content__wrap {
  padding: 0;
  padding-bottom: 4px;
}
</style>
