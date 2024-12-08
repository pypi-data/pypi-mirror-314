/**
 * Mixin to provide shared functionality needed to send updated participation data to the server
 */
import { createPersonalNotes } from "../personal_notes/personal_notes.graphql";
import { updateParticipationStatuses } from "./participationStatus.graphql";
import mutateMixin from "aleksis.core/mixins/mutateMixin.js";

export default {
  mixins: [mutateMixin],
  methods: {
    sendToServer(participations, field, value) {
      let fieldValue;

      if (field === "absenceReason") {
        fieldValue = {
          absenceReason: value === "present" ? null : value,
        };
      } else if (field === "tardiness") {
        fieldValue = {
          tardiness: value,
        };
      } else if (field === "extraMark") {
        // Too much different logic → own method
        this.addExtraMarks(participations, value);
        return;
      } else {
        console.error(`Wrong field '${field}' for sendToServer`);
        return;
      }

      this.beforeSendToServer(participations, field, value);

      this.mutate(
        updateParticipationStatuses,
        {
          input: participations.map((participation) => ({
            id: participation?.id || participation,
            ...fieldValue,
          })),
        },
        (storedDocumentations, incomingStatuses) => {
          // TODO: what should happen here in places where there is more than one documentation?
          const documentation = storedDocumentations.find(
            (doc) => doc.id === this.documentation.id,
          );

          incomingStatuses.forEach((newStatus) => {
            const participationStatus = documentation.participations.find(
              (part) => part.id === newStatus.id,
            );
            participationStatus.absenceReason = newStatus.absenceReason;
            participationStatus.tardiness = newStatus.tardiness;
            participationStatus.isOptimistic = newStatus.isOptimistic;
          });

          this.duringUpdateSendToServer(
            participations,
            field,
            value,
            incomingStatuses,
          );

          return storedDocumentations;
        },
      );

      this.afterSendToServer(participations, field, value);
    },
    addExtraMarks(participations, extraMarkId) {
      // Get all participation statuses without this extra mark and get the respective person ids
      const participants = participations
        .filter(
          (participation) =>
            !participation.notesWithExtraMark.some(
              (note) => note.extraMark.id === extraMarkId,
            ),
        )
        .map((participation) => participation.person.id);

      // CREATE new personal note
      this.mutate(
        createPersonalNotes,
        {
          input: participants.map((person) => ({
            documentation: this.documentation.id,
            person: person,
            extraMark: extraMarkId,
          })),
        },
        (storedDocumentations, incomingPersonalNotes) => {
          const documentation = storedDocumentations.find(
            (doc) => doc.id === this.documentation.id,
          );
          incomingPersonalNotes.forEach((note, index) => {
            const participationStatus = documentation.participations.find(
              (part) => part.person.id === participants[index],
            );
            participationStatus.notesWithExtraMark.push(note);
          });

          return storedDocumentations;
        },
      );
    },
    beforeSendToServer(_participations, _field, _value) {
      // Noop hook
    },
    duringUpdateSendToServer(_participations, _field, _value, _incoming) {
      // Noop hook
    },
    afterSendToServer(_participations, _field, _value) {
      // Noop hook
    },
  },
};
