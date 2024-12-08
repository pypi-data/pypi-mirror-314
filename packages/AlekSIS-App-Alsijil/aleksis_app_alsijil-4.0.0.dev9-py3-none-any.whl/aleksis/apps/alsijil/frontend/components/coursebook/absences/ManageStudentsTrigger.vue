<script>
import { DateTime } from "luxon";
import ManageStudentsDialog from "./ManageStudentsDialog.vue";
import documentationPartMixin from "../documentation/documentationPartMixin";
import { touchDocumentation } from "./participationStatus.graphql";
import mutateMixin from "aleksis.core/mixins/mutateMixin.js";

export default {
  name: "ManageStudentsTrigger",
  components: { ManageStudentsDialog },
  mixins: [documentationPartMixin, mutateMixin],
  data() {
    return {
      canOpenParticipation: false,
      timeout: null,
    };
  },
  props: {
    labelKey: {
      type: String,
      required: false,
      default: undefined,
    },
  },
  mounted() {
    const lessonStart = DateTime.fromISO(this.documentation.datetimeStart);
    const now = DateTime.now();
    this.canOpenParticipation = now >= lessonStart;

    if (!this.canOpenParticipation) {
      this.timeout = setTimeout(
        () => (this.canOpenParticipation = true),
        lessonStart.diff(now).toObject().milliseconds,
      );
    }
  },
  beforeDestroy() {
    if (this.timeout) {
      clearTimeout(this.timeout);
    }
  },
  methods: {
    touchDocumentation() {
      this.mutate(
        touchDocumentation,
        {
          documentationId: this.documentation.id,
        },
        (storedDocumentations, incoming) => {
          // ID may be different now
          return storedDocumentations.map((doc) =>
            doc.id === this.documentation.id
              ? Object.assign(doc, incoming, { oldId: doc.id })
              : doc,
          );
        },
      );
    },
  },
  computed: {
    showLabel() {
      return !!this.labelKey || !this.canOpenParticipation;
    },
    innerLabelKey() {
      if (this.documentation.futureNoticeParticipationStatus) {
        return "alsijil.coursebook.notes.future";
      }
      return this.labelKey;
    },
  },
};
</script>

<template>
  <manage-students-dialog
    v-bind="documentationPartProps"
    @update="() => null"
    :loading-indicator="loading"
    v-if="!documentation.amends?.cancelled"
  >
    <template #activator="{ attrs, on }">
      <v-chip
        dense
        color="primary"
        outlined
        :disabled="!canOpenParticipation || loading"
        v-bind="attrs"
        v-on="on"
        @click="touchDocumentation"
      >
        <v-icon :left="showLabel">mdi-account-edit-outline</v-icon>
        <template v-if="showLabel">
          {{ $t(innerLabelKey) }}
        </template>
      </v-chip>
    </template>
  </manage-students-dialog>
</template>

<style scoped></style>
