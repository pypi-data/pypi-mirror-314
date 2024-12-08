<template>
  <mobile-fullscreen-dialog v-model="popup" persistent :close-button="false">
    <template #activator="activator">
      <fab-button
        color="secondary"
        @click="popup = true"
        :disabled="popup"
        :class="{
          'd-none': !checkPermission('alsijil.view_register_absence_rule'),
        }"
        icon-text="$plus"
        i18n-key="alsijil.coursebook.absences.button"
      >
        <v-icon>$plus</v-icon>
      </fab-button>
    </template>
    <template #title>
      <div>
        {{ $t("alsijil.coursebook.absences.title") }}
      </div>
      <span v-if="!form" class="px-2">·</span>
      <div v-if="!form">
        {{ $t("alsijil.coursebook.absences.summary") }}
      </div>
    </template>
    <template #content>
      <absence-creation-form
        :persons="persons"
        :start-date="startDate"
        :end-date="endDate"
        :comment="comment"
        :absence-reason="absenceReason"
        :absence-reasons="absenceReasons"
        @valid="formValid = $event"
        @persons="persons = $event"
        @start-date="startDate = $event"
        @end-date="endDate = $event"
        @comment="comment = $event"
        @absence-reason="absenceReason = $event"
        :class="{
          'd-none': !form,
        }"
      />
      <absence-creation-summary
        v-if="!form"
        :persons="persons"
        :start-date="startDate"
        :end-date="endDate"
        @loading="handleLoading"
      />
    </template>
    <template #actionsLeft>
      <cancel-button @click="cancel" />
    </template>
    <template #actions>
      <!-- secondary -->
      <secondary-action-button
        @click="form = true"
        v-if="!form"
        :disabled="loading"
        i18n-key="actions.back"
      >
        <v-icon left>$prev</v-icon>
        {{ $t("actions.back") }}
      </secondary-action-button>
      <!-- primary -->
      <save-button
        v-if="form"
        @click="form = false"
        :loading="loading"
        :disabled="!formValid || !absenceReason"
      >
        {{ $t("actions.continue") }}
        <v-icon right>$next</v-icon>
      </save-button>
      <save-button
        v-else
        i18n-key="actions.confirm"
        @click="confirm"
        :loading="loading"
      />
    </template>
  </mobile-fullscreen-dialog>
</template>

<script>
import MobileFullscreenDialog from "aleksis.core/components/generic/dialogs/MobileFullscreenDialog.vue";
import AbsenceCreationForm from "./AbsenceCreationForm.vue";
import AbsenceCreationSummary from "./AbsenceCreationSummary.vue";
import FabButton from "aleksis.core/components/generic/buttons/FabButton.vue";
import CancelButton from "aleksis.core/components/generic/buttons/CancelButton.vue";
import SaveButton from "aleksis.core/components/generic/buttons/SaveButton.vue";
import SecondaryActionButton from "aleksis.core/components/generic/buttons/SecondaryActionButton.vue";
import loadingMixin from "aleksis.core/mixins/loadingMixin.js";
import permissionsMixin from "aleksis.core/mixins/permissions.js";
import mutateMixin from "aleksis.core/mixins/mutateMixin.js";
import { DateTime } from "luxon";

import { createAbsencesForPersons } from "./absenceCreation.graphql";

export default {
  name: "AbsenceCreationDialog",
  components: {
    MobileFullscreenDialog,
    AbsenceCreationForm,
    AbsenceCreationSummary,
    CancelButton,
    SaveButton,
    SecondaryActionButton,
    FabButton,
  },
  mixins: [loadingMixin, mutateMixin, permissionsMixin],
  data() {
    return {
      popup: false,
      form: true,
      formValid: false,
      persons: [],
      startDate: "",
      endDate: "",
      comment: "",
      absenceReason: "",
    };
  },
  props: {
    absenceReasons: {
      type: Array,
      required: true,
    },
  },
  mounted() {
    this.addPermissions(["alsijil.view_register_absence_rule"]);
    this.clearForm();
  },
  methods: {
    cancel() {
      this.popup = false;
      this.form = true;
      this.clearForm();
    },
    clearForm() {
      this.persons = [];
      this.startDate = DateTime.now()
        .startOf("day")
        .toISO({ suppressSeconds: true });
      this.endDate = DateTime.now()
        .endOf("day")
        .toISO({ suppressSeconds: true });
      this.comment = "";
      this.absenceReason = "";
    },
    confirm() {
      this.handleLoading(true);
      this.mutate(
        createAbsencesForPersons,
        {
          persons: this.persons.map((p) => p.id),
          start: this.$toUTCISO(this.$parseISODate(this.startDate)),
          end: this.$toUTCISO(this.$parseISODate(this.endDate)),
          comment: this.comment,
          reason: this.absenceReason,
        },
        (storedDocumentations, incomingStatuses) => {
          incomingStatuses.forEach((newStatus) => {
            const documentation = storedDocumentations.find(
              (doc) => doc.id === newStatus.relatedDocumentation.id,
            );
            if (!documentation) {
              return;
            }
            const participationStatus = documentation.participations.find(
              (part) => part.id === newStatus.id,
            );

            participationStatus.absenceReason = newStatus.absenceReason;
            participationStatus.isOptimistic = newStatus.isOptimistic;
          });

          return storedDocumentations;
        },
      );
      this.$once("save", this.handleSave);
    },
    handleSave() {
      this.cancel();
      this.$toastSuccess(this.$t("alsijil.coursebook.absences.success"));
    },
  },
};
</script>
