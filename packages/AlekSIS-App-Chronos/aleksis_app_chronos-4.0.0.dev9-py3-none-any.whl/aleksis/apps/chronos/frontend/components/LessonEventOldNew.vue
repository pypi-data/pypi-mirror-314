<script>
import LessonEventLinkIterator from "./LessonEventLinkIterator.vue";

export default {
  name: "LessonEventOldNew",
  components: { LessonEventLinkIterator },
  props: {
    oldItems: {
      type: Array,
      required: true,
    },
    newItems: {
      type: Array,
      required: true,
    },
    attr: {
      type: String,
      required: false,
      default: "name",
    },
  },
};
</script>

<template>
  <span v-bind="$attrs">
    <span v-if="oldItems.length > 0 && newItems.length > 0">
      <span class="text-decoration-line-through"
        ><lesson-event-link-iterator :items="oldItems" :attr="attr"
      /></span>
      <!-- eslint-disable-next-line @intlify/vue-i18n/no-raw-text -->
      <span> → </span>
      <lesson-event-link-iterator :items="newItems" :attr="attr" />
    </span>
    <span v-else-if="newItems.length > 0">
      <lesson-event-link-iterator :items="newItems" :attr="attr" />
    </span>
    <span v-else>
      <lesson-event-link-iterator :items="oldItems" :attr="attr" />
    </span>
  </span>
</template>
