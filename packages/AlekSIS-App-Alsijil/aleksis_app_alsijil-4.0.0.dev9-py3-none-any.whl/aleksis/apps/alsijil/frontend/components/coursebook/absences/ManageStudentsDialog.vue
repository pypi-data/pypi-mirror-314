<script>
import AbsenceReasonButtons from "aleksis.apps.kolego/components/AbsenceReasonButtons.vue";
import AbsenceReasonChip from "aleksis.apps.kolego/components/AbsenceReasonChip.vue";
import AbsenceReasonGroupSelect from "aleksis.apps.kolego/components/AbsenceReasonGroupSelect.vue";
import DialogCloseButton from "aleksis.core/components/generic/buttons/DialogCloseButton.vue";
import SecondaryActionButton from "aleksis.core/components/generic/buttons/SecondaryActionButton.vue";
import MobileFullscreenDialog from "aleksis.core/components/generic/dialogs/MobileFullscreenDialog.vue";
import updateParticipationMixin from "./updateParticipationMixin.js";
import deepSearchMixin from "aleksis.core/mixins/deepSearchMixin.js";
import LessonInformation from "../documentation/LessonInformation.vue";
import {
  extendParticipationStatuses,
  updateParticipationStatuses,
} from "./participationStatus.graphql";
import SlideIterator from "aleksis.core/components/generic/SlideIterator.vue";
import PersonalNotes from "../personal_notes/PersonalNotes.vue";
import PersonalNoteChip from "../personal_notes/PersonalNoteChip.vue";
import ExtraMarkChip from "../../extra_marks/ExtraMarkChip.vue";
import TardinessChip from "./TardinessChip.vue";
import TardinessField from "./TardinessField.vue";
import ExtraMarkButtons from "../../extra_marks/ExtraMarkButtons.vue";
import MessageBox from "aleksis.core/components/generic/MessageBox.vue";

export default {
  name: "ManageStudentsDialog",
  extends: MobileFullscreenDialog,
  components: {
    ExtraMarkButtons,
    TardinessChip,
    ExtraMarkChip,
    AbsenceReasonChip,
    AbsenceReasonGroupSelect,
    AbsenceReasonButtons,
    PersonalNotes,
    PersonalNoteChip,
    LessonInformation,
    MessageBox,
    MobileFullscreenDialog,
    SecondaryActionButton,
    SlideIterator,
    TardinessField,
    DialogCloseButton,
  },
  mixins: [updateParticipationMixin, deepSearchMixin],
  data() {
    return {
      dialog: false,
      search: "",
      loadSelected: false,
      selected: [],
      isExpanded: false,
      markAsAbsentDay: {
        showAlert: false,
        num: 0,
        reason: "no reason",
        name: "nobody",
        participationIDs: [],
        loading: false,
      },
    };
  },
  props: {
    loadingIndicator: {
      type: Boolean,
      default: false,
      required: false,
    },
    useDeepSearch: {
      type: Boolean,
      default: true,
      required: false,
    },
  },
  computed: {
    items() {
      return this.documentation.participations;
    },
  },
  methods: {
    handleMultipleAction(field, id) {
      this.loadSelected = true;
      this.sendToServer(this.selected, field, id);
      this.$once("save", this.resetMultipleAction);
    },
    resetMultipleAction() {
      this.loadSelected = false;
      this.$set(this.selected, []);
      this.$refs.iterator.selected = [];
    },
    activateFullDayDialog(items) {
      const itemIds = items.map((item) => item.id);
      const participations = this.documentation.participations.filter((part) =>
        itemIds.includes(part.id),
      );

      if (this.markAsAbsentDay.num === 1) {
        this.markAsAbsentDay.name = participations[0].person.firstName;
      }

      this.$set(this.markAsAbsentDay, "participationIDs", itemIds);

      this.markAsAbsentDay.loading = false;
      this.markAsAbsentDay.showAlert = true;
    },
    beforeSendToServer() {
      this.markAsAbsentDay.showAlert = false;
      this.markAsAbsentDay.participationIDs = [];
    },
    duringUpdateSendToServer(
      _participations,
      _field,
      _value,
      incomingStatuses,
    ) {
      this.markAsAbsentDay.reason = incomingStatuses[0].absenceReason?.name;
      this.markAsAbsentDay.num = incomingStatuses.length;
    },
    afterSendToServer(_participations, field, value) {
      if (field === "absenceReason" && value !== "present") {
        this.$once("save", this.activateFullDayDialog);
      }
    },
    markAsAbsentDayClick() {
      this.markAsAbsentDay.loading = true;

      this.mutate(
        extendParticipationStatuses,
        {
          input: this.markAsAbsentDay.participationIDs,
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

          this.markAsAbsentDay.reason = "no reason";
          this.markAsAbsentDay.num = 0;
          this.markAsAbsentDay.participationIDs = [];
          this.markAsAbsentDay.loading = false;

          this.markAsAbsentDay.showAlert = false;

          return storedDocumentations;
        },
      );
    },
  },
};
</script>

<template>
  <mobile-fullscreen-dialog
    scrollable
    v-bind="$attrs"
    v-on="$listeners"
    v-model="dialog"
    :close-button="false"
  >
    <template #activator="activator">
      <slot name="activator" v-bind="activator" />
    </template>

    <template #title>
      <div class="d-flex full-width">
        <lesson-information v-bind="documentationPartProps" :compact="false" />
        <dialog-close-button @click="dialog = false" class="ml-4" />
      </div>
      <v-scroll-x-transition leave-absolute>
        <v-text-field
          v-show="!isExpanded"
          type="search"
          v-model="search"
          clearable
          rounded
          hide-details
          single-line
          prepend-inner-icon="$search"
          dense
          outlined
          :placeholder="$t('actions.search')"
          class="pt-4 full-width"
        />
      </v-scroll-x-transition>
      <message-box
        v-model="markAsAbsentDay.showAlert"
        color="success"
        icon="$success"
        transition="slide-y-transition"
        dismissible
        class="mt-4 mb-0 full-width"
      >
        <div class="text-subtitle-2">
          {{
            $tc(
              "alsijil.coursebook.mark_as_absent_day.title",
              markAsAbsentDay.num,
              markAsAbsentDay,
            )
          }}
        </div>
        <p class="text-body-2 pa-0 ma-0" style="word-break: break-word">
          {{
            $t(
              "alsijil.coursebook.mark_as_absent_day.description",
              markAsAbsentDay,
            )
          }}
        </p>

        <secondary-action-button
          color="success"
          i18n-key="alsijil.coursebook.mark_as_absent_day.action_button"
          class="mt-2"
          :loading="markAsAbsentDay.loading"
          @click="markAsAbsentDayClick"
        />
      </message-box>
    </template>
    <template #content>
      <slide-iterator
        ref="iterator"
        v-model="selected"
        :items="items"
        :search="search"
        :item-key-getter="
          (item) => 'documentation-' + documentation.id + '-student-' + item.id
        "
        :is-expanded.sync="isExpanded"
        :loading="loadingIndicator || loadSelected"
        :load-only-selected="loadSelected"
        :disabled="loading"
        :custom-filter="deepSearch"
      >
        <template #listItemContent="{ item }">
          <v-list-item-title>
            {{ item.person.fullName }}
          </v-list-item-title>
          <v-list-item-subtitle
            v-if="
              item.absenceReason ||
              item.notesWithNote?.length > 0 ||
              item.notesWithExtraMark?.length > 0 ||
              item.tardiness
            "
            class="d-flex flex-wrap gap"
          >
            <absence-reason-chip
              v-if="item.absenceReason"
              small
              :absence-reason="item.absenceReason"
            />
            <personal-note-chip
              v-for="note in item.notesWithNote"
              :key="'text-note-note-overview-' + note.id"
              :note="note"
              small
            />
            <extra-mark-chip
              v-for="note in item.notesWithExtraMark"
              :key="'extra-mark-note-overview-' + note.id"
              :extra-mark="extraMarks.find((e) => e.id === note.extraMark.id)"
              small
            />
            <tardiness-chip
              v-if="item.tardiness"
              :tardiness="item.tardiness"
              small
            />
          </v-list-item-subtitle>
        </template>

        <template #expandedItem="{ item, close }">
          <v-card-title>
            <v-tooltip bottom>
              <template #activator="{ on, attrs }">
                <v-btn v-bind="attrs" v-on="on" icon @click="close">
                  <v-icon>$prev</v-icon>
                </v-btn>
              </template>
              <span v-t="'actions.back_to_overview'" />
            </v-tooltip>
            {{ item.person.fullName }}
            <v-spacer />
            <v-tooltip bottom>
              <template #activator="{ on, attrs }">
                <v-btn
                  v-bind="attrs"
                  v-on="on"
                  icon
                  :to="{
                    name: 'core.personById',
                    params: {
                      id: item.person.id,
                    },
                  }"
                >
                  <v-icon>mdi-open-in-new</v-icon>
                </v-btn>
              </template>
              {{ $t("actions.open_person_page", item.person) }}
            </v-tooltip>
          </v-card-title>
          <v-card-text>
            <absence-reason-group-select
              allow-empty
              :load-selected-chip="loading"
              :value="item.absenceReason?.id || 'present'"
              :custom-absence-reasons="absenceReasons"
              @input="sendToServer([item], 'absenceReason', $event)"
            />
            <tardiness-field
              v-bind="documentationPartProps"
              :loading="loading"
              :disabled="loading"
              :participations="[item]"
              :value="item.tardiness"
              @input="sendToServer([item], 'tardiness', $event)"
            />
          </v-card-text>
          <v-divider />
          <v-card-text>
            <personal-notes
              v-bind="documentationPartProps"
              :participation="
                documentation.participations.find((p) => p.id === item.id)
              "
            />
          </v-card-text>
        </template>
      </slide-iterator>
    </template>

    <template #actions>
      <v-scroll-y-reverse-transition>
        <div v-show="selected.length > 0" class="full-width">
          <h4>{{ $t("alsijil.coursebook.participation_status") }}</h4>
          <absence-reason-buttons
            class="mb-1"
            allow-empty
            empty-value="present"
            :custom-absence-reasons="absenceReasons"
            @input="handleMultipleAction('absenceReason', $event)"
          />
          <h4>{{ $t("alsijil.extra_marks.title_plural") }}</h4>
          <extra-mark-buttons
            :custom-extra-marks="extraMarks"
            @input="handleMultipleAction('extraMark', $event)"
          />
          <h4>{{ $t("alsijil.personal_notes.tardiness") }}</h4>
          <tardiness-field
            v-bind="documentationPartProps"
            :loading="loading"
            :disabled="loading"
            :value="0"
            :participations="selected"
            @input="handleMultipleAction('tardiness', $event)"
          />
        </div>
      </v-scroll-y-reverse-transition>
    </template>
  </mobile-fullscreen-dialog>
</template>

<style scoped></style>
