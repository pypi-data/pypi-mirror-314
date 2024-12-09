<script>
export default {
  name: "LessonEventSubject",
  props: {
    event: {
      type: Object,
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
    <span
      v-if="
        event.meta.subject && event.meta.amended && event.meta.amends.subject
      "
    >
      <span class="text-decoration-line-through">
        {{ event.meta.amends.subject[attr] }}</span
      >
      <!-- eslint-disable-next-line @intlify/vue-i18n/no-raw-text -->
      <span> → </span>
      <span>{{ event.meta.subject[attr] }}</span>
    </span>
    <span v-else-if="event.meta.subject">
      {{ event.meta.subject[attr] }}
    </span>
    <span v-else-if="event.meta.amended && event.meta.amends.subject">
      {{ event.meta.amends.subject[attr] }}
    </span>
    <span v-else>
      {{ event["name"] }}
    </span>
  </span>
</template>
