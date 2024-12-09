<script>
import Mascot from "aleksis.core/components/generic/mascot/Mascot.vue";

export default {
  name: "NoTimetableCard",
  components: { Mascot },
  props: {
    titleKey: {
      type: String,
      required: false,
      default: "chronos.timetable.no_timetable_selected.title",
    },
    descriptionKey: {
      type: String,
      required: false,
      default: "chronos.timetable.no_timetable_selected.description",
    },
  },
};
</script>

<template>
  <v-card
    class="full-height d-flex align-center justify-center py-10"
    v-bind="$attrs"
  >
    <div class="text-center">
      <mascot
        type="timetable"
        class="mb-4"
        max-width="min(80vw, 600px)"
        max-height="min(50vh, 500px)"
        contain
      />
      <div class="text-h5 grey--text text--darken-2 mb-2">
        {{ $t(titleKey) }}
      </div>
      <div
        class="text-body-2 grey--text text--darken-2"
        v-if="$vuetify.breakpoint.lgAndUp"
      >
        {{ $t(descriptionKey) }}
      </div>
      <div v-if="$vuetify.breakpoint.mdAndDown">
        <v-btn color="primary" @click="$emit('selectTimetable')" class="mt-4">
          {{ $t("chronos.timetable.select") }}
        </v-btn>
      </div>
    </div>
  </v-card>
</template>
