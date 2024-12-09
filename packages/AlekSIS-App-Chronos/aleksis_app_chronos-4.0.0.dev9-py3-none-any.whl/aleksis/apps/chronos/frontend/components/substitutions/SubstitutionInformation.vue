<script setup>
import SubstitutionStatus from "./SubstitutionStatus.vue";

import { DateTime } from "luxon";
</script>

<template>
  <div class="full-width grid">
    <div class="d-flex">
      <substitution-status :substitution="substitution" />
      <div class="text-right d-flex flex-column fit-content">
        <time :datetime="substitution.datetimeStart" class="text-no-wrap">
          {{ $d(toDateTime(substitution.datetimeStart), "shortTime") }}
        </time>
        <time :datetime="substitution.datetimeEnd" class="text-no-wrap">
          {{ $d(toDateTime(substitution.datetimeEnd), "shortTime") }}
        </time>
      </div>
    </div>
    <span class="text-subtitle-1 font-weight-medium">
      {{ course?.name }}
    </span>
  </div>
</template>

<script>
export default {
  name: "SubstitutionInformation",
  props: {
    substitution: {
      type: Object,
      required: true,
    },
  },
  methods: {
    toDateTime(dateString) {
      return DateTime.fromISO(dateString);
    },
  },
  computed: {
    course() {
      if (this.substitution.course) {
        return this.substitution.course;
      } else if (this.substitution.amends?.course) {
        return this.substitution.amends.course;
      }
      return undefined;
    },
  },
};
</script>

<style scoped>
.grid {
  display: grid;
  align-items: center;
  gap: 1em;
  grid-template-columns: 1fr 1fr;
  align-content: unset;
}

.grid:last-child {
  justify-self: end;
  justify-content: end;
}

.fit-content {
  width: fit-content;
}

.gap {
  gap: 0.25em;
}
</style>
