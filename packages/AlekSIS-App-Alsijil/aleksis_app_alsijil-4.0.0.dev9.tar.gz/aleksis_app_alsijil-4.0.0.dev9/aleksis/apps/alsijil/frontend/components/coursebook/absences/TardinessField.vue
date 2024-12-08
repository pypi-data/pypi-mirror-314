<script>
import { DateTime } from "luxon";
import documentationPartMixin from "../documentation/documentationPartMixin";
import ConfirmDialog from "aleksis.core/components/generic/dialogs/ConfirmDialog.vue";
import formRulesMixin from "aleksis.core/mixins/formRulesMixin.js";

export default {
  name: "TardinessField",
  components: { ConfirmDialog },
  mixins: [documentationPartMixin, formRulesMixin],
  props: {
    value: {
      type: Number,
      default: null,
      required: false,
    },
    participations: {
      type: Array,
      required: true,
    },
  },
  computed: {
    lessonLength() {
      const lessonStart = DateTime.fromISO(this.documentation.datetimeStart);
      const lessonEnd = DateTime.fromISO(this.documentation.datetimeEnd);

      let diff = lessonEnd.diff(lessonStart, "minutes");
      return diff.toObject().minutes;
    },
    defaultTimes() {
      const lessonStart = DateTime.fromISO(this.documentation.datetimeStart);
      const lessonEnd = DateTime.fromISO(this.documentation.datetimeEnd);
      const now = DateTime.now();

      let current = [];

      if (now >= lessonStart && now <= lessonEnd) {
        const diff = parseInt(
          now.diff(lessonStart, "minutes").toObject().minutes,
        );

        current.push({
          text: diff,
          value: diff,
          current: true,
        });
      }

      return current.concat([
        {
          text: 5,
          value: 5,
        },
        {
          text: 10,
          value: 10,
        },
        {
          text: 15,
          value: 15,
        },
      ]);
    },
  },
  methods: {
    lessonLengthRule(time) {
      return (
        time == null ||
        time <= this.lessonLength ||
        this.$t("alsijil.personal_notes.lesson_length_exceeded")
      );
    },
    saveValue(value) {
      this.$emit("input", value);
      this.previousValue = value;
    },
    confirm() {
      this.saveValue(0);
    },
    cancel() {
      this.saveValue(this.previousValue);
    },
    processValueObjectOptional(value) {
      if (Object.hasOwn(value, "value")) {
        return value.value;
      }

      return value;
    },
    set(newValue) {
      newValue = this.processValueObjectOptional(newValue);

      if (!newValue || parseInt(newValue) === 0) {
        // this is a DELETE action, show the dialog, ...
        this.showDeleteConfirm = true;
        return;
      }

      this.saveValue(parseInt(newValue));
    },
  },
  data() {
    return {
      showDeleteConfirm: false,
      previousValue: 0,
    };
  },
  mounted() {
    this.previousValue = this.value;
  },
};
</script>

<template>
  <v-combobox
    outlined
    class="mt-1"
    prepend-inner-icon="mdi-clock-alert-outline"
    :suffix="$t('time.minutes')"
    :label="$t('alsijil.personal_notes.tardiness')"
    :rules="
      $rules()
        .isANumber.isAWholeNumber.isGreaterThan(0)
        .build([lessonLengthRule])
        .map((f) => (v) => f(this.processValueObjectOptional(v)))
    "
    :items="defaultTimes"
    :value="value"
    @change="set($event)"
    v-bind="$attrs"
  >
    <template #item="{ item }">
      <v-list-item-icon v-if="item.current">
        <v-icon>mdi-shimmer</v-icon>
      </v-list-item-icon>
      <v-list-item-content>
        <v-list-item-title>
          {{
            $tc(
              item.current
                ? "alsijil.personal_notes.minutes_late_current"
                : "time.minutes_n",
              item.value,
            )
          }}
        </v-list-item-title>
      </v-list-item-content>
    </template>
    <template #append>
      <confirm-dialog
        v-model="showDeleteConfirm"
        @confirm="confirm"
        @cancel="cancel"
      >
        <template #title>
          {{ $t("alsijil.personal_notes.confirm_delete") }}
        </template>
        <template #text>
          {{
            $t("alsijil.personal_notes.confirm_delete_tardiness", {
              tardiness: previousValue,
              name: participations.map((p) => p.person.firstName).join(", "),
            })
          }}
        </template>
      </confirm-dialog>
    </template>
  </v-combobox>
</template>

<style scoped>
.mt-n1-5 {
  margin-top: -6px;
}
</style>
