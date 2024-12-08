<script setup>
import AbsenceReasonChip from "aleksis.apps.kolego/components/AbsenceReasonChip.vue";
import ExtraMarkChip from "../../extra_marks/ExtraMarkChip.vue";
import ExtraMarksNote from "../personal_notes/ExtraMarksNote.vue";
import TardinessChip from "../absences/TardinessChip.vue";
import PersonalNoteChip from "../personal_notes/PersonalNoteChip.vue";
import TextNoteCard from "../personal_notes/TextNoteCard.vue";
</script>

<template>
  <div>
    <div
      class="d-flex align-center justify-space-between justify-md-end flex-wrap gap"
      v-if="compact || documentation.canViewParticipationStatus"
    >
      <v-chip
        dense
        color="success"
        outlined
        v-if="total > 0 && documentation.canViewParticipationStatus"
      >
        {{
          $t("alsijil.coursebook.participations.present_number", {
            present,
            total,
          })
        }}
      </v-chip>
      <v-chip
        dense
        color="success"
        outlined
        @click="$emit('open')"
        v-bind="dialogActivator.attrs"
        v-on="dialogActivator.on"
        v-else-if="
          total == 1 &&
          present == 1 &&
          !documentation.canViewParticipationStatus
        "
      >
        {{ $t("alsijil.coursebook.participations.present") }}
      </v-chip>

      <template v-if="documentation.canViewParticipationStatus">
        <absence-reason-chip
          v-for="[reasonId, participations] in Object.entries(absences)"
          :key="'reason-' + reasonId"
          :absence-reason="participations[0].absenceReason"
          dense
        >
          <template #append>
            <span
              >:
              <span>
                {{
                  participations
                    .slice(0, 5)
                    .map((participation) => participation.person.firstName)
                    .join(", ")
                }}
              </span>
              <span v-if="participations.length > 5">
                <!-- eslint-disable @intlify/vue-i18n/no-raw-text -->
                +{{ participations.length - 5 }}
                <!-- eslint-enable @intlify/vue-i18n/no-raw-text -->
              </span>
            </span>
          </template>
        </absence-reason-chip>
      </template>
      <template v-else>
        <absence-reason-chip
          v-for="[reasonId, participations] in Object.entries(absences)"
          :key="'reason-' + reasonId"
          :absence-reason="participations[0].absenceReason"
          dense
          @click="$emit('open')"
          v-bind="dialogActivator.attrs"
          v-on="dialogActivator.on"
        />
      </template>

      <template v-if="documentation.canViewParticipationStatus">
        <extra-mark-chip
          v-for="[markId, [mark, ...participations]] in Object.entries(
            extraMarkChips,
          )"
          :key="'extra-mark-' + markId"
          :extra-mark="mark"
          dense
        >
          <template #append>
            <span
              >:
              <span>
                {{
                  participations
                    .slice(0, 5)
                    .map((participation) => participation.person.firstName)
                    .join(", ")
                }}
              </span>
              <span v-if="participations.length > 5">
                <!-- eslint-disable @intlify/vue-i18n/no-raw-text -->
                +{{ participations.length - 5 }}
                <!-- eslint-enable @intlify/vue-i18n/no-raw-text -->
              </span>
            </span>
          </template>
        </extra-mark-chip>
      </template>
      <template v-else>
        <extra-mark-chip
          v-for="[markId, [mark, ...participations]] in Object.entries(
            extraMarkChips,
          )"
          :key="'extra-mark-' + markId"
          :extra-mark="mark"
          dense
          @click="$emit('open')"
          v-bind="dialogActivator.attrs"
          v-on="dialogActivator.on"
        />
      </template>

      <template v-if="documentation.canViewParticipationStatus">
        <tardiness-chip v-if="tardyParticipations.length > 0">
          <template #default>
            {{ $t("alsijil.personal_notes.late") }}
          </template>

          <template #append>
            <span
              >:
              {{
                tardyParticipations
                  .slice(0, 5)
                  .map((participation) => participation.person.firstName)
                  .join(", ")
              }}

              <span v-if="tardyParticipations.length > 5">
                <!-- eslint-disable @intlify/vue-i18n/no-raw-text -->
                +{{ tardyParticipations.length - 5 }}
                <!-- eslint-enable @intlify/vue-i18n/no-raw-text -->
              </span>
            </span>
          </template>
        </tardiness-chip>
      </template>
      <template v-else>
        <tardiness-chip
          v-if="tardyParticipations.length > 0"
          :tardiness="
            tardyParticipations.length == 1
              ? tardyParticipations[0].tardiness
              : undefined
          "
          @click="$emit('open')"
          v-bind="dialogActivator.attrs"
          v-on="dialogActivator.on"
        />
      </template>

      <template v-if="!documentation.canViewParticipationStatus && total == 1">
        <personal-note-chip
          v-for="note in documentation?.participations[0]?.notesWithNote"
          :key="'text-note-note-' + note.id"
          :note="note"
          @click="$emit('open')"
          v-bind="dialogActivator.attrs"
          v-on="dialogActivator.on"
        />
      </template>

      <manage-students-trigger
        v-if="documentation.canEditParticipationStatus"
        :label-key="manageStudentsLabelKey"
        v-bind="documentationPartProps"
      />
    </div>

    <!-- not compact -->
    <div class="main-body" v-else>
      <template
        v-if="
          tardyParticipations.length > 0 || Object.entries(absences).length > 0
        "
      >
        <v-divider />
        <div
          class="d-flex align-center justify-space-between justify-md-end flex-wrap gap"
        >
          <tardiness-chip
            v-if="tardyParticipations.length > 0"
            :tardiness="
              tardyParticipations.length == 1
                ? tardyParticipations[0].tardiness
                : undefined
            "
          />
          <absence-reason-chip
            v-for="[reasonId, participations] in Object.entries(absences)"
            :key="'reason-' + reasonId"
            :absence-reason="participations[0].absenceReason"
            dense
          />
        </div>
      </template>
      <template v-if="total == 1">
        <v-divider />
        <extra-marks-note
          v-bind="documentationPartProps"
          :participation="documentation?.participations[0]"
          :value="documentation?.participations[0].notesWithExtraMark"
          :disabled="true"
        />
      </template>
      <template
        v-if="
          total == 1 &&
          documentation?.participations[0]?.notesWithNote.length > 0
        "
      >
        <v-divider />
        <div>
          <text-note-card
            v-for="note in documentation?.participations[0]?.notesWithNote"
            :key="'text-note-note-' + note.id"
            :note="note"
          />
        </div>
      </template>
    </div>
  </div>
</template>

<script>
import documentationPartMixin from "./documentationPartMixin";
import ManageStudentsTrigger from "../absences/ManageStudentsTrigger.vue";

export default {
  name: "LessonNotes",
  components: { ManageStudentsTrigger },
  mixins: [documentationPartMixin],
  computed: {
    total() {
      return this.documentation.participations.length;
    },
    /**
     * Return the number of present people.
     */
    present() {
      return this.documentation.participations.filter(
        (p) => p.absenceReason === null,
      ).length;
    },
    /**
     * Get all course attendants who have an absence reason, grouped by that reason.
     */
    absences() {
      return Object.groupBy(
        this.documentation.participations.filter(
          (p) => p.absenceReason !== null,
        ),
        ({ absenceReason }) => absenceReason.id,
      );
    },
    /**
     * Parse and combine all extraMark notes.
     *
     * Notes with extraMarks are grouped by ExtraMark. ExtraMarks with the showInCoursebook property set to false are ignored.
     * @return An object where the keys are extraMark IDs and the values have the structure [extraMark, note1, note2, ..., noteN]
     */
    extraMarkChips() {
      // Apply the inner function to each participation, with value being the resulting object
      return this.documentation.participations.reduce((value, p) => {
        // Go through every extra mark of this participation
        for (const { extraMark } of p.notesWithExtraMark) {
          // Only proceed if the extraMark should be displayed here
          if (!extraMark.showInCoursebook) {
            continue;
          }

          // value[extraMark.id] is an Array with the structure [extraMark, note1, note2, ..., noteN]
          if (value[extraMark.id]) {
            value[extraMark.id].push(p);
          } else {
            value[extraMark.id] = [
              this.extraMarks.find((e) => e.id === extraMark.id),
              p,
            ];
          }
        }

        return value;
      }, {});
    },
    /**
     * Return a list Participations with a set tardiness
     */
    tardyParticipations() {
      return this.documentation.participations.filter((p) => p.tardiness);
    },
    manageStudentsLabelKey() {
      if (this.total == 0) {
        return "alsijil.coursebook.notes.show_list";
      }
      return "";
    },
  },
};
</script>

<style scoped>
.gap {
  gap: 0.25em;
}
.main-body {
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  gap: 1em;
}
</style>
