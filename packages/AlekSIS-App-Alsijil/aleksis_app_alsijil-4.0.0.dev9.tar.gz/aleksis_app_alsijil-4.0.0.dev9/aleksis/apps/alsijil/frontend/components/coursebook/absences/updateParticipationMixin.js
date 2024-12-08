/**
 * Mixin to provide shared functionality needed to update participations
 */
import documentationPartMixin from "../documentation/documentationPartMixin";
import sendToServerMixin from "./sendToServerMixin";

export default {
  mixins: [documentationPartMixin, sendToServerMixin],
};
