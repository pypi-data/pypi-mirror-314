<template>
  <base-calendar-feed-details
    v-bind="$props"
    :color="currentSubject ? currentSubject.colour_bg : null"
    without-location
  >
    <template #title>
      <slot name="title">
        <div
          :style="{
            color: currentSubject
              ? currentSubject.colour_fg || 'white'
              : 'white',
          }"
        >
          <lesson-event-subject :event="selectedEvent" />
        </div>
      </slot>
    </template>
    <template #badge>
      <cancelled-calendar-status-chip
        v-if="selectedEvent.meta.cancelled"
        class="ml-4"
      />
      <calendar-status-chip
        color="warning"
        icon="mdi-clipboard-alert-outline"
        v-else-if="selectedEvent.meta.amended"
        class="ml-4"
      >
        {{ $t("chronos.event.current_changes") }}
      </calendar-status-chip>
    </template>
    <template #description>
      <v-divider inset />
      <v-list-item v-if="selectedEvent.meta.groups.length > 0">
        <v-list-item-icon>
          <v-icon color="primary">mdi-account-group-outline</v-icon>
        </v-list-item-icon>
        <v-list-item-content>
          <v-list-item-title>
            <lesson-related-object-chip
              v-for="group in selectedEvent.meta.groups"
              :key="group.id"
              >{{ group.name }}</lesson-related-object-chip
            >
          </v-list-item-title>
        </v-list-item-content>
      </v-list-item>
      <v-list-item>
        <v-list-item-icon>
          <v-icon color="primary">mdi-human-male-board </v-icon>
        </v-list-item-icon>
        <v-list-item-content>
          <v-list-item-title>
            <span v-if="teachers.length === 0" class="body-2 text--secondary">{{
              $t("chronos.event.no_teacher")
            }}</span>
            <lesson-related-object-chip
              v-for="teacher in teachers"
              :status="teacher.status"
              :key="teacher.id"
              new-icon="mdi-account-plus-outline"
              >{{ teacher.full_name }}</lesson-related-object-chip
            >
          </v-list-item-title>
        </v-list-item-content>
      </v-list-item>
      <v-list-item>
        <v-list-item-icon>
          <v-icon color="primary">mdi-door </v-icon>
        </v-list-item-icon>
        <v-list-item-content>
          <v-list-item-title>
            <span v-if="rooms.length === 0" class="body-2 text--secondary">{{
              $t("chronos.event.no_room")
            }}</span>
            <lesson-related-object-chip
              v-for="room in rooms"
              :status="room.status"
              :key="room.id"
              new-icon="mdi-door-open"
              >{{ room.name }}</lesson-related-object-chip
            >
          </v-list-item-title>
        </v-list-item-content>
      </v-list-item>
      <v-divider inset />
      <v-list-item v-if="selectedEvent.meta.comment">
        <v-list-item-content>
          <v-list-item-title>
            <v-alert
              dense
              outlined
              type="warning"
              icon="mdi-information-outline"
            >
              {{ selectedEvent.meta.comment }}
            </v-alert>
          </v-list-item-title>
        </v-list-item-content>
      </v-list-item>
      <amend-lesson
        v-if="selectedEvent"
        :selected-event="selectedEvent"
        @refreshCalendar="$emit('refreshCalendar')"
      />
    </template>
  </base-calendar-feed-details>
</template>

<script>
import calendarFeedDetailsMixin from "aleksis.core/mixins/calendarFeedDetails.js";
import BaseCalendarFeedDetails from "aleksis.core/components/calendar/BaseCalendarFeedDetails.vue";
import CalendarStatusChip from "aleksis.core/components/calendar/CalendarStatusChip.vue";
import CancelledCalendarStatusChip from "aleksis.core/components/calendar/CancelledCalendarStatusChip.vue";

import LessonRelatedObjectChip from "../../LessonRelatedObjectChip.vue";

import lessonEvent from "../mixins/lessonEvent";
import LessonEventSubject from "../../LessonEventSubject.vue";

import AmendLesson from "../../AmendLesson.vue";

export default {
  name: "LessonDetails",
  components: {
    LessonEventSubject,
    LessonRelatedObjectChip,
    BaseCalendarFeedDetails,
    CalendarStatusChip,
    CancelledCalendarStatusChip,
    AmendLesson,
  },
  mixins: [calendarFeedDetailsMixin, lessonEvent],
};
</script>
