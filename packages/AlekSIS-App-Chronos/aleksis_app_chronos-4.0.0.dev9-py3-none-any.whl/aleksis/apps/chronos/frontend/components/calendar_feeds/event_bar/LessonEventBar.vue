<template>
  <base-calendar-feed-event-bar
    :with-padding="false"
    :without-time="true"
    v-bind="$props"
  >
    <template #icon> </template>

    <template #title>
      <div
        class="d-flex justify-start"
        :class="{
          'px-1': true,
          'current-changes':
            selectedEvent.meta.amended && !selectedEvent.meta.cancelled,
          cancelled: selectedEvent.meta.cancelled,
          'text-decoration-line-through': selectedEvent.meta.cancelled,
        }"
        :style="{
          color: currentSubject ? currentSubject.colour_fg || 'white' : 'white',
          height: '100%',
          borderRadius: '4px',
        }"
      >
        <span
          v-if="calendarType === 'month' && eventParsed.start.hasTime"
          class="mr-1 font-weight-bold ml-1"
        >
          {{ eventParsed.start.time }}
        </span>
        <div
          class="d-flex justify-center align-center flex-grow-1 text-truncate"
        >
          <div class="d-flex justify-center align-center flex-wrap text">
            <slot name="additionalElements"></slot>

            <lesson-event-link-iterator
              v-if="!selectedEvent.meta.is_member"
              :items="selectedEvent.meta.groups"
              attr="short_name"
              class="mr-1"
            />
            <lesson-event-old-new
              v-if="!selectedEvent.meta.is_teacher || newTeachers.length > 0"
              :new-items="newTeachers"
              :old-items="oldTeachers"
              attr="short_name"
              class="mr-1"
            />

            <lesson-event-subject
              v-if="withSubject"
              :event="selectedEvent"
              attr="short_name"
              class="font-weight-medium mr-1"
            />
            <lesson-event-old-new
              :new-items="newRooms"
              :old-items="oldRooms"
              attr="short_name"
            />
          </div>
        </div>
      </div>
    </template>
  </base-calendar-feed-event-bar>
</template>

<script>
import calendarFeedEventBarMixin from "aleksis.core/mixins/calendarFeedEventBar.js";
import BaseCalendarFeedEventBar from "aleksis.core/components/calendar/BaseCalendarFeedEventBar.vue";
import lessonEvent from "../mixins/lessonEvent";
import LessonEventSubject from "../../LessonEventSubject.vue";
import LessonEventLinkIterator from "../../LessonEventLinkIterator.vue";
import LessonEventOldNew from "../../LessonEventOldNew.vue";

export default {
  name: "LessonEventBar",
  components: {
    LessonEventOldNew,
    LessonEventLinkIterator,
    LessonEventSubject,
    BaseCalendarFeedEventBar,
  },
  computed: {
    selectedEvent() {
      return this.event;
    },
  },
  props: {
    withSubject: {
      type: Boolean,
      default: true,
      required: false,
    },
  },
  mixins: [calendarFeedEventBarMixin, lessonEvent],
};
</script>

<style scoped>
.current-changes {
  border: 3px orange solid;
}

.cancelled {
  border: 3px red solid;
}

.text {
  line-height: 1.1;
  font-size: 12px;
}
</style>
