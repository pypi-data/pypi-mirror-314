<template>
  <v-form @input="$emit('valid', $event)">
    <v-container>
      <v-row>
        <div aria-required="true" class="full-width">
          <!-- FIXME Vue 3: clear-on-select -->
          <v-autocomplete
            :label="$t('forms.labels.persons')"
            :items="allPersons"
            item-text="fullName"
            return-object
            multiple
            chips
            deletable-chips
            :rules="
              $rules().build([
                (value) => value.length > 0 || $t('forms.errors.required'),
              ])
            "
            :value="persons"
            :loading="$apollo.queries.allPersons.loading"
            @input="$emit('persons', $event)"
          />
        </div>
      </v-row>
      <v-row>
        <v-col cols="12" :sm="6" class="pl-0">
          <div aria-required="true">
            <date-time-field
              :label="$t('forms.labels.start')"
              :max-date="endDate"
              :max-time="maxStartTime"
              :rules="$rules().required.build()"
              :value="startDate"
              @input="$emit('start-date', $event)"
            />
          </div>
        </v-col>
        <v-col cols="12" :sm="6" class="pr-0">
          <div aria-required="true">
            <date-time-field
              :label="$t('forms.labels.end')"
              :min-date="startDate"
              :min-time="minEndTime"
              :rules="$rules().required.build()"
              :value="endDate"
              @input="$emit('end-date', $event)"
            />
          </div>
        </v-col>
      </v-row>
      <v-row>
        <v-text-field
          :label="$t('forms.labels.comment')"
          :value="comment"
          @input="$emit('comment', $event)"
        />
      </v-row>
      <v-row>
        <div aria-required="true">
          <absence-reason-group-select
            :rules="$rules().required.build()"
            :value="absenceReason"
            :custom-absence-reasons="absenceReasons"
            @input="$emit('absence-reason', $event)"
          />
        </div>
      </v-row>
    </v-container>
  </v-form>
</template>

<script>
import AbsenceReasonGroupSelect from "aleksis.apps.kolego/components/AbsenceReasonGroupSelect.vue";
import DateTimeField from "aleksis.core/components/generic/forms/DateTimeField.vue";
import { persons } from "./absenceCreation.graphql";
import formRulesMixin from "aleksis.core/mixins/formRulesMixin.js";
import { DateTime } from "luxon";

export default {
  name: "AbsenceCreationForm",
  components: {
    AbsenceReasonGroupSelect,
    DateTimeField,
  },
  mixins: [formRulesMixin],
  emits: [
    "valid",
    "persons",
    "start-date",
    "end-date",
    "comment",
    "absence-reason",
  ],
  apollo: {
    allPersons: persons,
  },
  props: {
    persons: {
      type: Array,
      required: true,
    },
    startDate: {
      type: String,
      required: true,
    },
    endDate: {
      type: String,
      required: true,
    },
    comment: {
      type: String,
      required: true,
    },
    absenceReason: {
      type: String,
      required: true,
    },
    absenceReasons: {
      type: Array,
      required: true,
    },
  },
  computed: {
    maxStartTime() {
      // Only if on the same day
      const start = DateTime.fromISO(this.startDate);
      const end = DateTime.fromISO(this.endDate);

      if (start.day !== end.day) return;

      return end.minus({ minutes: 5 }).toFormat("HH:mm");
    },
    minEndTime() {
      // Only if on the same day
      const start = DateTime.fromISO(this.startDate);
      const end = DateTime.fromISO(this.endDate);

      if (start.day !== end.day) return;

      return start.plus({ minutes: 5 }).toFormat("HH:mm");
    },
  },
};
</script>
