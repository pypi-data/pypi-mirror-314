<template>
  <div>
    <!-- compact -->
    <div
      class="d-flex flex-column flex-md-row align-stretch align-md-center gap justify-start fill-height"
      v-if="compact"
    >
      <documentation-compact-details
        v-bind="dialogActivator.attrs"
        v-on="dialogActivator.on"
        v-if="
          !documentation.canEdit &&
          (documentation.topic ||
            documentation.homework ||
            documentation.groupNote)
        "
        :documentation="documentation"
        @click="$emit('open')"
        :class="{
          'flex-grow-1 min-width pa-1 read-only-grid': true,
          'full-width': $vuetify.breakpoint.mobile,
        }"
      />
      <v-alert
        v-else-if="documentation.futureNotice"
        type="warning"
        outlined
        class="min-width flex-grow-1 mb-0"
      >
        {{ $t("alsijil.coursebook.notices.future") }}
      </v-alert>
      <v-alert
        v-else-if="!documentation.canEdit"
        type="info"
        outlined
        class="min-width flex-grow-1 mb-0"
      >
        {{ $t("alsijil.coursebook.notices.no_entry") }}
      </v-alert>

      <v-text-field
        v-if="documentation.canEdit"
        :class="{
          'flex-grow-1 min-width': true,
          'full-width': $vuetify.breakpoint.mobile,
        }"
        hide-details
        outlined
        :label="$t('alsijil.coursebook.summary.topic.label')"
        :value="documentation.topic"
        @input="topic = $event"
        @focusout="save"
        @keydown.enter="saveAndBlur"
        :loading="loading"
      >
        <template #append>
          <v-tooltip bottom>
            <template #activator="{ on, attrs }">
              <v-scroll-x-transition>
                <v-icon
                  v-if="appendIcon"
                  :color="appendIconColor"
                  v-on="on"
                  v-bind="attrs"
                  >{{ appendIcon }}</v-icon
                >
              </v-scroll-x-transition>
            </template>
            <span>{{ appendIconTooltip }}</span>
          </v-tooltip>
        </template>
      </v-text-field>
      <div
        :class="{
          'flex-grow-1 max-width': true,
          'full-width': $vuetify.breakpoint.mobile,
        }"
        v-if="documentation.canEdit"
      >
        <v-card
          v-bind="dialogActivator.attrs"
          v-on="dialogActivator.on"
          outlined
          @click="$emit('open')"
          class="max-width grid-layout pa-1"
          dense
          rounded="lg"
        >
          <span class="max-width text-truncate">{{
            documentation.homework
              ? $t("alsijil.coursebook.summary.homework.value", documentation)
              : $t("alsijil.coursebook.summary.homework.empty")
          }}</span>
          <v-icon right class="float-right">{{ homeworkIcon }}</v-icon>
          <span class="max-width text-truncate">{{
            documentation.groupNote
              ? $t("alsijil.coursebook.summary.group_note.value", documentation)
              : $t("alsijil.coursebook.summary.group_note.empty")
          }}</span>
          <v-icon right class="float-right">{{ groupNoteIcon }}</v-icon>
        </v-card>
      </div>
    </div>
    <!-- not compact -->
    <!-- Are focusout & enter enough trigger? -->
    <v-text-field
      filled
      v-if="!compact && documentation.canEdit"
      :label="$t('alsijil.coursebook.summary.topic.label')"
      :value="documentation.topic"
      @input="topic = $event"
    />
    <v-textarea
      filled
      auto-grow
      rows="3"
      clearable
      v-if="!compact && documentation.canEdit"
      :label="$t('alsijil.coursebook.summary.homework.label')"
      :value="documentation.homework"
      @input="homework = $event ? $event : ''"
    />
    <v-textarea
      filled
      auto-grow
      rows="3"
      clearable
      v-if="!compact && documentation.canEdit"
      :label="$t('alsijil.coursebook.summary.group_note.label')"
      :value="documentation.groupNote"
      @input="groupNote = $event ? $event : ''"
    />

    <documentation-full-details
      v-if="!compact && !documentation.canEdit"
      :documentation="documentation"
    />
  </div>
</template>

<script setup>
import DocumentationCompactDetails from "./DocumentationCompactDetails.vue";
import DocumentationFullDetails from "./DocumentationFullDetails.vue";
</script>

<script>
import createOrPatchMixin from "aleksis.core/mixins/createOrPatchMixin.js";
import documentationPartMixin from "./documentationPartMixin";
import documentationCacheUpdateMixin from "./documentationCacheUpdateMixin";

export default {
  name: "LessonSummary",
  mixins: [
    createOrPatchMixin,
    documentationCacheUpdateMixin,
    documentationPartMixin,
  ],
  emits: ["open", "dirty"],
  data() {
    return {
      topic: null,
      homework: null,
      groupNote: null,
      appendIcon: null,
      topicError: null,
    };
  },
  methods: {
    handleAppendIconSuccess() {
      this.topicError = null;
      this.appendIcon = "$success";
      setTimeout(() => {
        this.appendIcon = "";
      }, 3000);
    },
    save() {
      if (
        this.topic !== null ||
        this.homework !== null ||
        this.groupNote !== null
      ) {
        this.createOrPatch([
          {
            id: this.documentation.id,
            ...(this.topic !== null && { topic: this.topic }),
            ...(this.homework !== null && { homework: this.homework }),
            ...(this.groupNote !== null && { groupNote: this.groupNote }),
          },
        ]);

        this.topic = null;
        this.homework = null;
        this.groupNote = null;
      }
    },
    saveAndBlur(event) {
      this.save();
      event.target.blur();
    },
    handleError(error) {
      this.appendIcon = "$error";
      this.topicError = error;
    },
  },
  computed: {
    homeworkIcon() {
      if (this.documentation.homework) {
        return this.documentation.canEdit
          ? "mdi-book-edit-outline"
          : "mdi-book-alert-outline";
      }
      return this.documentation.canEdit
        ? "mdi-book-plus-outline"
        : "mdi-book-off-outline";
    },
    groupNoteIcon() {
      if (this.documentation.groupNote) {
        return this.documentation.canEdit
          ? "mdi-note-edit-outline"
          : "mdi-note-alert-outline";
      }
      return this.documentation.canEdit
        ? "mdi-note-plus-outline"
        : "mdi-note-off-outline";
    },
    minWidth() {
      return Math.min(this.documentation?.topic?.length || 15, 15) + "ch";
    },
    maxWidth() {
      return this.$vuetify.breakpoint.mobile ? "100%" : "20ch";
    },
    appendIconColor() {
      return (
        { $success: "success", $error: "error" }[this.appendIcon] || "primary"
      );
    },
    appendIconTooltip() {
      return (
        {
          $success: this.$t("alsijil.coursebook.summary.topic.status.success"),
          $error: this.$t("alsijil.coursebook.summary.topic.status.error", {
            error: this.topicError,
          }),
        }[this.appendIcon] || ""
      );
    },
    dirty() {
      return !(
        this.topic === this.documentation.topic &&
        this.homework === this.documentation.homework &&
        this.groupNote === this.documentation.groupNote
      );
    },
  },
  mounted() {
    this.$on("save", this.handleAppendIconSuccess);

    this.topic = this.documentation.topic;
    this.homework = this.documentation.homework;
    this.groupNote = this.documentation.groupNote;
  },
  watch: {
    dirty(dirty) {
      this.$emit("dirty", dirty);
    },
  },
};
</script>

<style scoped>
.min-width {
  min-width: v-bind(minWidth);
}

.max-width {
  max-width: v-bind(maxWidth);
}

.gap {
  gap: 1em;
}

.grid-layout {
  display: grid;
  grid-template-columns: auto min-content;
}

.read-only-grid {
  display: grid;
  grid-template-columns: min-content auto;
  grid-template-rows: auto;
}
</style>
