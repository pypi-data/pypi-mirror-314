<script setup>
import SubstitutionInformation from "./SubstitutionInformation.vue";
import TeacherField from "aleksis.apps.cursus/components/TeacherField.vue";
import SubjectChipSelectField from "aleksis.apps.cursus/components/SubjectChipSelectField.vue";

import createOrPatchMixin from "aleksis.core/mixins/createOrPatchMixin.js";
import deleteMixin from "aleksis.core/mixins/deleteMixin.js";
</script>

<template>
  <v-card class="my-1 full-width" :loading="loading">
    <v-card-text
      class="full-width main-body pa-2"
      :class="{
        vertical: $vuetify.breakpoint.mobile,
      }"
    >
      <substitution-information :substitution="substitution" />

      <subject-chip-select-field
        :value="subject"
        :disabled="loading"
        :items="amendableSubjects"
        @input="subjectInput"
      />

      <v-autocomplete
        :value="substitutionRoomIDs"
        multiple
        chips
        deletable-chips
        dense
        hide-details
        outlined
        :items="amendableRooms"
        item-text="name"
        item-value="id"
        :disabled="loading"
        :label="$t('chronos.substitutions.overview.rooms.label')"
        @input="roomsInput"
      >
        <template #prepend-inner>
          <template
            v-if="roomsWithStatus.filter((t) => t.status === 'regular').length"
          >
            <v-chip
              v-for="room in roomsWithStatus.filter(
                (t) => t.status === 'regular',
              )"
              :key="room.id"
              class="mb-1"
              small
            >
              {{ room.shortName }}
            </v-chip>
          </template>
          <template
            v-if="roomsWithStatus.filter((t) => t.status === 'removed').length"
          >
            <v-chip
              v-for="room in roomsWithStatus.filter(
                (t) => t.status === 'removed',
              )"
              :key="room.id"
              outlined
              color="error"
              class="mb-1"
              small
            >
              <v-icon left small>mdi-cancel</v-icon>
              <div class="text-decoration-line-through">
                {{ room.shortName ? room.shortName : room.name }}
              </div>
            </v-chip>
          </template>
        </template>
        <template #selection="data">
          <v-chip
            v-bind="data.attrs"
            :input-value="data.selected"
            v-if="getRoomStatus(data.item) === 'new'"
            close
            class="mb-1 mt-1"
            small
            outlined
            color="success"
            @click:close="removeRoom(data.item)"
          >
            <v-icon left small> mdi-plus </v-icon>
            {{ data.item.shortName ? data.item.shortName : data.item.name }}
          </v-chip>
        </template>
      </v-autocomplete>

      <teacher-field
        v-if="amendableTeachers.length > 0"
        :priority-subject="subject"
        :show-subjects="true"
        :value="substitutionTeacherIDs"
        chips
        deletable-chips
        dense
        hide-details
        outlined
        :disabled="loading"
        :label="$t('chronos.substitutions.overview.teacher.label')"
        :custom-teachers="amendableTeachers"
        @input="teachersInput"
      >
        <template #prepend-inner>
          <v-tooltip bottom>
            <template #activator="{ on, attrs }">
              <v-chip
                v-for="teacher in teachersWithStatus.filter(
                  (t) => t.status === 'removed',
                )"
                :key="teacher.id"
                outlined
                color="error"
                class="mb-1"
                small
                v-on="on"
                v-bind="attrs"
              >
                <v-icon left small>mdi-account-off-outline</v-icon>
                <div class="text-decoration-line-through">
                  {{ teacher.fullName }}
                </div>
              </v-chip>
            </template>
            <span>{{
              $t("chronos.substitutions.overview.teacher.status.absent")
            }}</span>
          </v-tooltip>
        </template>
        <template #selection="data">
          <v-tooltip bottom>
            <template #activator="{ on, attrs }">
              <v-chip
                v-bind="{ ...data.attrs, ...attrs }"
                :input-value="data.selected"
                close
                class="mb-1 mt-1"
                small
                :outlined="getTeacherStatus(data.item) === 'new'"
                :color="getTeacherStatus(data.item) === 'new' ? 'success' : ''"
                @click:close="removeTeacher(data.item)"
                v-on="on"
              >
                <v-icon left small v-if="getTeacherStatus(data.item) === 'new'">
                  mdi-account-plus-outline
                </v-icon>
                {{ data.item.fullName }}
              </v-chip>
            </template>
            <span>{{
              getTeacherStatus(data.item) === "new"
                ? $t("chronos.substitutions.overview.teacher.status.new")
                : $t("chronos.substitutions.overview.teacher.status.regular")
            }}</span>
          </v-tooltip>
        </template>
      </teacher-field>

      <v-text-field
        dense
        outlined
        hide-details
        :label="$t('chronos.substitutions.overview.comment')"
        :value="substitution.comment"
        @input="comment = $event"
        @focusout="save(false)"
        @keydown.enter="save(false)"
      />

      <v-btn-toggle
        mandatory
        dense
        :color="substitution.cancelled ? 'error' : 'success'"
        :disabled="loading"
        class="justify-self-end"
        :value="substitution.cancelled"
        @change="save(false)"
      >
        <v-btn outlined :value="false" @click="cancelled = false">
          {{ $t("chronos.substitutions.overview.cancel.not_cancelled") }}
        </v-btn>
        <v-btn outlined :value="true" @click="cancelled = true">
          {{ $t("chronos.substitutions.overview.cancel.cancelled") }}
        </v-btn>
      </v-btn-toggle>
    </v-card-text>
    <v-divider />
  </v-card>
</template>

<script>
export default {
  name: "SubstitutionCard",
  emits: ["open", "close", "delete"],
  mixins: [createOrPatchMixin, deleteMixin],
  data() {
    return {
      loading: false,
      teachers: [],
      rooms: [],
      substitutionSubject: null,
      comment: null,
      cancelled: null,
    };
  },
  props: {
    substitution: {
      type: Object,
      required: true,
    },
    amendableRooms: {
      type: Array,
      required: false,
      default: () => [],
    },
    amendableSubjects: {
      type: Array,
      required: false,
      default: () => [],
    },
    amendableTeachers: {
      type: Array,
      required: false,
      default: () => [],
    },
  },
  methods: {
    handleUpdateAfterCreateOrPatch(itemId) {
      return (cached, incoming) => {
        for (const object of incoming) {
          console.log("summary: handleUpdateAfterCreateOrPatch", object);
          // Replace the current substitution
          const index = cached.findIndex(
            (o) => o[itemId] === this.substitution.id,
          );
          // merged with the incoming partial substitution
          // if creation of proper substitution from dummy one, set ID of substitution currently being edited as oldID so that key in overview doesn't change
          cached[index] = {
            ...this.substitution,
            ...object,
            oldId:
              this.substitution.id !== object.id
                ? this.substitution.id
                : this.substitution.oldId,
          };
        }
        return cached;
      };
    },
    handleUpdateAfterDelete(ids, itemId) {
      return (cached, incoming) => {
        for (const id of ids) {
          // Remove item from cached data or reset it to old ID, if present
          const index = cached.findIndex((o) => o[itemId] === id);
          if (cached[index].oldId) {
            cached[index].id = cached[index].oldId;
            cached[index].oldId = null;

            // Clear dummy substitution
            cached[index].teachers = [];
            cached[index].rooms = [];
            cached[index].subject = null;
            cached[index].comment = "";
            cached[index].cancelled = false;
          } else {
            this.$emit("delete", cached[index].datetimeStart);
          }
        }
        return cached;
      };
    },
    getTeacherStatus(teacher) {
      return this.teachersWithStatus.find((t) => t.id === teacher.id)?.status;
    },
    getRoomStatus(room) {
      return this.roomsWithStatus.find((r) => r.id === room.id)?.status;
    },
    removeTeacher(teacher) {
      this.teachers = this.substitutionTeacherIDs.filter(
        (t) => t !== teacher.id,
      );
      this.save(true);
    },
    removeRoom(room) {
      this.rooms = this.substitutionRoomIDs.filter((r) => r !== room.id);
      this.save(true);
    },
    subjectInput(subject) {
      this.substitutionSubject = subject.id;
      this.save();
    },
    teachersInput(teachers) {
      this.teachers = teachers;
      this.save();
    },
    roomsInput(rooms) {
      this.rooms = rooms;
      this.save();
    },
    cancelledInput(cancelled) {
      this.cancelled = cancelled;
      this.save();
    },
    save(allowEmpty = false) {
      if (
        this.teachers.length ||
        this.rooms.length ||
        this.substitutionSubject !== null ||
        (this.comment !== null && this.comment !== "") ||
        this.cancelled !== null
      ) {
        this.createOrPatch([
          {
            id: this.substitution.id,
            ...((allowEmpty || this.teachers.length) && {
              teachers: this.teachers,
            }),
            ...((allowEmpty || this.rooms.length) && { rooms: this.rooms }),
            ...(this.substitutionSubject !== null && {
              subject: this.substitutionSubject,
            }),
            ...(this.comment !== null &&
              this.comment !== "" && { comment: this.comment }),
            ...(this.cancelled !== null && { cancelled: this.cancelled }),
            ...((this.teachers.length || this.rooms.length) && {
              cancelled: false,
            }),
          },
        ]);
        this.teachers = [];
        this.rooms = [];
        this.substitutionSubject = null;
        this.comment = null;
        this.cancelled = null;
      } else if (!this.substitution.id.startsWith("DUMMY")) {
        this.delete([this.substitution]);
      }
    },
  },
  computed: {
    substitutionTeacherIDs() {
      return this.substitution.teachers.map((teacher) => teacher.id);
    },
    substitutionRoomIDs() {
      return this.substitution.rooms.map((room) => room.id);
    },
    // Group teachers by their substitution status (regular, new, removed)
    teachersWithStatus() {
      // IDs of teachers of amended lesson
      const oldIds = this.substitution.amends.teachers.map(
        (teacher) => teacher.id,
      );
      // IDs of teachers of new substitution lesson
      const newIds = this.substitution.teachers.map((teacher) => teacher.id);
      const allTeachers = new Set(
        this.substitution.amends.teachers.concat(this.substitution.teachers),
      );
      let teachersWithStatus = Array.from(allTeachers).map((teacher) => {
        let status = "regular";
        if (newIds.includes(teacher.id) && !oldIds.includes(teacher.id)) {
          // Mark teacher as being new if they are only linked to the substitution lesson
          status = "new";
        } else if (
          !newIds.includes(teacher.id) &&
          oldIds.includes(teacher.id)
        ) {
          // Mark teacher as being rremoved if they are only linked to the amended lesson
          status = "removed";
        }
        return { ...teacher, status: status };
      });
      return teachersWithStatus;
    },
    roomsWithStatus() {
      const oldIds = this.substitution.amends.rooms.map((room) => room.id);
      const newIds = this.substitution.rooms.map((room) => room.id);
      const allRooms = new Set(
        this.substitution.amends.rooms.concat(
          this.substitution.rooms.filter((r) => !oldIds.includes(r.id)),
        ),
      );
      let roomsWithStatus = Array.from(allRooms).map((room) => {
        let status = "regular";
        if (newIds.includes(room.id) && !oldIds.includes(room.id)) {
          status = "new";
        } else if (
          newIds.length &&
          !newIds.includes(room.id) &&
          oldIds.includes(room.id)
        ) {
          status = "removed";
        }
        return { ...room, status: status };
      });
      return roomsWithStatus;
    },
    subject() {
      if (this.substitution.subject) {
        return this.substitution.subject;
      } else if (this.substitution.course?.subject) {
        return this.substitution.course.subject;
      } else if (this.substitution.amends?.subject) {
        return this.substitution.amends.subject;
      }
      return undefined;
    },
  },
};
</script>

<style scoped>
.main-body {
  display: grid;
  align-items: center;
  grid-template-columns: 2fr 1fr 2fr 3fr 1fr 2fr;
  gap: 1em;
}
.vertical {
  grid-template-columns: 1fr;
}
.justify-self-end {
  justify-self: end;
}
</style>
