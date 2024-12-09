<template>
  <lesson-details v-bind="$attrs" v-on="$listeners">
    <template #title>
      <v-icon class="mr-1">mdi-coffee</v-icon>
      {{ $t("chronos.supervisions.title") }}
    </template>
  </lesson-details>
</template>

<script>
import LessonDetails from "./LessonDetails.vue";

export default {
  name: "SupervisionDetails",
  extends: [LessonDetails],
  components: {
    LessonDetails,
  },
};
</script>
