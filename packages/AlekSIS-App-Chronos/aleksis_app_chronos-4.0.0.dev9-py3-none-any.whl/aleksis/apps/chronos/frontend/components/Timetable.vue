<script setup>
import TimetableWrapper from "./TimetableWrapper.vue";
</script>

<script>
import { DateTime } from "luxon";
import { gqlTimetableDays } from "./timetables.graphql";

export default {
  name: "Timetable",
  data() {
    return {
      calendarFocus: "",
      calendarType: "week",
      initialRouteFocusSet: false,
      timetableDays: [1, 2, 3, 4, 5],
    };
  },
  methods: {
    setCalendarFocus(val) {
      this.calendarFocus = val;
    },
    setCalendarType(val) {
      this.calendarType = val;
    },
    setInnerFocusAndType() {
      if (this.$route.name === "chronos.timetableWithId") {
        this.$refs.calendarWithControls.setCalendarFocus(
          DateTime.now().toISODate(),
        );
        this.$refs.calendarWithControls.setCalendarType(
          this.$vuetify.breakpoint.mdAndDown ? "day" : "week",
        );
      } else {
        this.initialRouteFocusSet = true;
        this.$refs.calendarWithControls.setCalendarFocus(
          [
            this.$route.params.year,
            this.$route.params.month,
            this.$route.params.day,
          ].join("-"),
        );
        this.$refs.calendarWithControls.setCalendarType(
          this.$route.params.view,
        );
      }
    },
  },
  watch: {
    calendarFocus(newValue, oldValue) {
      // Do not redirect on first page load
      if (oldValue === "") return;

      // Do not redirect when calendar focus was just set with route param values
      if (this.initialRouteFocusSet) {
        this.initialRouteFocusSet = false;
        return;
      }

      const [year, month, day] = newValue.split("-");
      this.$router.push({
        name: "chronos.timetableWithIdAndParams",
        params: {
          view: this.calendarType,
          year,
          month,
          day,
        },
      });
    },
    calendarType(newValue) {
      const [year, month, day] = this.calendarFocus.split("-");
      this.$router.push({
        name: "chronos.timetableWithIdAndParams",
        params: {
          view: newValue,
          year,
          month,
          day,
        },
      });
    },
  },
  apollo: {
    timetableDays: {
      query: gqlTimetableDays,
    },
  },
};
</script>

<template>
  <timetable-wrapper>
    <template #default="{ selected }">
      <calendar-with-controls
        :calendar-feeds="[
          { name: 'lesson' },
          { name: 'supervision' },
          { name: 'holidays' },
        ]"
        :params="{ type: selected.type, id: selected.objId }"
        ref="calendarWithControls"
        :calendar-days-of-week="timetableDays"
        scroll-target="first"
        @changeCalendarFocus="setCalendarFocus"
        @changeCalendarType="setCalendarType"
        @calendarReady="setInnerFocusAndType"
      />
    </template>
  </timetable-wrapper>
</template>
