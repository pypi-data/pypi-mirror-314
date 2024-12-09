<template>
  <v-card-actions v-if="checkPermission('chronos.edit_substitution_rule')">
    <edit-button
      i18n-key="chronos.event.amend.edit_button"
      @click="edit = true"
    />
    <delete-button
      v-if="selectedEvent.meta.amended"
      i18n-key="chronos.event.amend.delete_button"
      @click="deleteEvent = true"
    />
    <dialog-object-form
      v-model="edit"
      :fields="fields"
      :is-create="!selectedEvent.meta.amended"
      create-item-i18n-key="chronos.event.amend.title"
      :gql-create-mutation="gqlCreateMutation"
      :get-create-data="transformCreateData"
      :default-item="defaultItem"
      edit-item-i18n-key="chronos.event.amend.title"
      :gql-patch-mutation="gqlPatchMutation"
      :get-patch-data="transformPatchData"
      :edit-item="initPatchData"
      @cancel="open = false"
      @save="updateOnSave()"
    >
      <!-- eslint-disable-next-line vue/valid-v-slot -->
      <template #subject.field="{ attrs, on, item }">
        <v-autocomplete
          :disabled="item.cancelled"
          :items="amendableSubjects"
          item-text="name"
          item-value="id"
          v-bind="attrs"
          v-on="on"
        />
      </template>
      <!-- eslint-disable-next-line vue/valid-v-slot -->
      <template #teachers.field="{ attrs, on, item }">
        <v-autocomplete
          :disabled="item.cancelled"
          multiple
          :items="amendableTeachers"
          item-text="fullName"
          item-value="id"
          v-bind="attrs"
          v-on="on"
          chips
          deletable-chips
        />
      </template>
      <!-- eslint-disable-next-line vue/valid-v-slot -->
      <template #rooms.field="{ attrs, on, item }">
        <v-autocomplete
          :disabled="item.cancelled"
          multiple
          :items="amendableRooms"
          item-text="name"
          item-value="id"
          v-bind="attrs"
          v-on="on"
          chips
          deletable-chips
        />
      </template>
      <!-- eslint-disable-next-line vue/valid-v-slot -->
      <template #cancelled.field="{ attrs, on }">
        <v-checkbox v-bind="attrs" v-on="on" />
      </template>
      <!-- eslint-disable-next-line vue/valid-v-slot -->
      <template #comment.field="{ attrs, on }">
        <v-textarea v-bind="attrs" v-on="on" />
      </template>
    </dialog-object-form>
    <delete-dialog
      delete-success-message-i18n-key="chronos.event.amend.delete_success"
      :gql-delete-mutation="gqlDeleteMutation"
      v-model="deleteEvent"
      :items="[selectedEvent.meta]"
      :get-name-of-item="getLessonDeleteText"
      @save="updateOnSave()"
    >
      <template #title>
        {{ $t("chronos.event.amend.delete_dialog") }}
      </template>
    </delete-dialog>
  </v-card-actions>
</template>

<script>
import permissionsMixin from "aleksis.core/mixins/permissions.js";
import EditButton from "aleksis.core/components/generic/buttons/EditButton.vue";
import DialogObjectForm from "aleksis.core/components/generic/dialogs/DialogObjectForm.vue";
import DeleteButton from "aleksis.core/components/generic/buttons/DeleteButton.vue";
import DeleteDialog from "aleksis.core/components/generic/dialogs/DeleteDialog.vue";
import {
  gqlSubjects,
  gqlPersons,
  gqlRooms,
  createAmendLessons,
  patchAmendLessons,
  deleteAmendLessons,
} from "./amendLesson.graphql";

export default {
  name: "AmendLesson",
  components: {
    EditButton,
    DialogObjectForm,
    DeleteButton,
    DeleteDialog,
  },
  mixins: [permissionsMixin],
  props: {
    selectedEvent: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      edit: false,
      fields: [
        {
          text: this.$t("chronos.event.amend.subject"),
          value: "subject",
        },
        {
          text: this.$t("chronos.event.amend.teachers"),
          value: "teachers",
        },
        {
          text: this.$t("chronos.event.amend.rooms"),
          value: "rooms",
        },
        {
          text: this.$t("chronos.event.amend.cancelled"),
          value: "cancelled",
        },
        {
          text: this.$t("chronos.event.amend.comment"),
          value: "comment",
        },
      ],
      defaultItem: {
        cancelled: this.selectedEvent.meta.cancelled,
        comment: this.selectedEvent.meta.comment,
      },
      gqlCreateMutation: createAmendLessons,
      gqlPatchMutation: patchAmendLessons,
      deleteEvent: false,
      gqlDeleteMutation: deleteAmendLessons,
    };
  },
  methods: {
    transformCreateData(item) {
      return {
        ...item,
        amends: this.selectedEvent.meta.id,
        datetimeStart: this.$toUTCISO(this.selectedEvent.startDateTime),
        datetimeEnd: this.$toUTCISO(this.selectedEvent.endDateTime),
        // Normalize cancelled, v-checkbox returns null & does not
        // honor false-value.
        cancelled: item.cancelled ? true : false,
      };
    },
    transformPatchData(item) {
      let { __typename, cancelled, ...patchItem } = item;
      return {
        ...patchItem,
        // Normalize cancelled, v-checkbox returns null & does not
        // honor false-value.
        cancelled: cancelled ? true : false,
      };
    },
    updateOnSave() {
      this.$emit("refreshCalendar");
      this.model = false;
    },
    getLessonDeleteText(item) {
      return `${this.selectedEvent.name} · ${this.$d(
        this.selectedEvent.start,
        "shortDateTime",
      )} – ${this.$d(this.selectedEvent.end, "shortTime")}`;
    },
  },
  computed: {
    initPatchData() {
      return {
        id: this.selectedEvent.meta.id,
        subject: this.selectedEvent.meta.subject?.id.toString(),
        teachers: this.selectedEvent.meta.teachers.map((teacher) =>
          teacher.id.toString(),
        ),
        rooms: this.selectedEvent.meta.rooms.map((room) => room.id.toString()),
        cancelled: this.selectedEvent.meta.cancelled,
        comment: this.selectedEvent.meta.comment,
      };
    },
  },
  apollo: {
    amendableSubjects: gqlSubjects,
    amendableTeachers: gqlPersons,
    amendableRooms: gqlRooms,
  },
  mounted() {
    this.addPermissions(["chronos.edit_substitution_rule"]);
  },
};
</script>
