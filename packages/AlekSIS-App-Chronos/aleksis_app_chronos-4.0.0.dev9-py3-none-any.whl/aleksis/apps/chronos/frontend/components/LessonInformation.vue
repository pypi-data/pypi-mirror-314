<script setup>
import CancelledCalendarStatusChip from "aleksis.core/components/calendar/CancelledCalendarStatusChip.vue";
import SubjectChip from "aleksis.apps.cursus/components/SubjectChip.vue";

import { DateTime } from "luxon";
</script>

<template>
  <v-card-text>
    <cancelled-calendar-status-chip v-if="lesson.cancelled" class="mr-2" />
    <div
      :class="{
        'text-decoration-line-through': lesson.cancelled,
        'text--secondary': lesson.cancelled,
      }"
    >
      {{ $d(toDateTime(lesson.datetimeStart), "shortTime") }} –
      {{ $d(toDateTime(lesson.datetimeEnd), "shortTime") }}
      {{ getCourse(lesson)?.name }}
    </div>
    <subject-chip v-if="getSubject(lesson)" :subject="getSubject(lesson)" />
  </v-card-text>
</template>

<script>
export default {
  name: "LessonInformation",
  props: {
    lesson: {
      type: Object,
      required: true,
    },
    cancelled: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  methods: {
    toDateTime(dateString) {
      return DateTime.fromISO(dateString);
    },
    getSubject(lesson) {
      if (lesson.subject) {
        return lesson.subject;
      } else if (lesson.course?.subject) {
        return lesson.course.subject;
      } else if (lesson.amends?.subject) {
        return lesson.amends.subject;
      }
      return undefined;
    },

    getCourse(lesson) {
      if (lesson.course) {
        return lesson.course;
      } else if (lesson.amends?.course) {
        return lesson.amends.course;
      }
      return undefined;
    },
  },
};
</script>
