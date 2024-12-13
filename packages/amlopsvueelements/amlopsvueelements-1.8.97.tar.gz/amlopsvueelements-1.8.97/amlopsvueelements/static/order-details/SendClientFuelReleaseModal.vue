<template>
  <div v-if="props.isOpen" class="order-modal">
    <div class="order-modal-wrapper">
      <div ref="target" class="order-modal-container">
        <div class="order-modal-body">
          <OrderForm add-default-classes is-modal>
            <template #header>
              <div class="header w-full flex justify-between">
                <div class="text-[1.25rem] font-medium text-grey-1000">
                  Send Client Fuel Release
                </div>
                <button @click.stop="emit('modal-close')">
                  <img
                    width="12"
                    height="12"
                    src="../../assets/icons/cross.svg"
                    alt="delete"
                    class="close"
                  />
                </button>
              </div>
            </template>
            <template #content>
              <div class="form-body-wrapper">
                <div class="flex gap-[12px] align-center">
                  <SelectField
                    v-model="recipients"
                    label-text="Recipients"
                    label="display"
                    :options="recipientOptions"
                    :required="true"
                    :multiple="true"
                    :errors="errors.recipients"
                  />
                  <!-- TODO: Uncomment once Add Additional Contact Detail page by @Denis Verbin is ready -->
                  <!-- <div class="add-recipient-btn">
                    <img
                      width="12"
                      height="12"
                      src="../../assets/icons/plus.svg"
                      alt="comment"
                      @click="onAddRecipient"
                    />
                  </div> -->
                </div>
                <SelectField
                  v-model="from"
                  label-text="From"
                  :required="true"
                  :options="[userEmail, 'fuelteam@amlglobal.net']"
                  :errors="errors.from"
                />
                <InputField
                  v-model="subject"
                  class="w-full"
                  label-text="Subject"
                  placeholder="Please enter subject"
                />
                <TextareaField
                  v-model="clientNote"
                  class="w-full"
                  label-text="Client Note"
                  placeholder="Please enter client note"
                />
                <Label label-text="Fuel Releases" :required="false"></Label>
                <div class="flex items-center justify-start pb-[0.75rem]">
                  <CheckboxField
                    v-model="sendAmlFuelRelease"
                    class="mb-0 mr-[6px]"
                    :size="'20px'"
                  />
                  <p class="whitespace-nowrap text-base-900 file-title">
                    AML Fuel Release {{ forCallsign }}
                  </p>
                </div>
                <div class="flex items-center justify-start pb-[0.75rem]">
                  <CheckboxField
                    v-model="sendSupplierFuelRelease"
                    class="mb-0 mr-[6px]"
                    :size="'20px'"
                  />
                  <!-- TODO: add $supplier_reference after callsign -->
                  <p class="whitespace-nowrap text-base-900 file-title">
                    Supplier Fuel Release {{ forCallsign }}
                  </p>
                </div>
              </div>
            </template>
          </OrderForm>
        </div>
        <div class="order-modal-footer">
          <Loading v-if="isLoading" class="mr-4" />
          <button class="modal-button cancel" @click.stop="emit('modal-close')">Cancel</button>
          <button
            class="modal-button submit"
            :disabled="isLoading || hasErrors"
            @click.stop="onSend()"
          >
            Submit
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { computed, ref, watch } from 'vue';
import { storeToRefs } from 'pinia';
import { Loading } from 'shared/components';
import { useOrderStore } from '@/stores/useOrderStore';
import { useUserStore } from '@/stores/useUserStore';
import OrderForm from '@/components/forms/OrderForm.vue';
import { useMutationSendFuelRelease } from '@/services/mutations/fuel';
import { useQueryClientQuoteAddresses, useQueryOrderClientDocuments } from '@/services/queries';
import { notify } from '@/helpers/toast';
import CheckboxField from '../forms/fields/CheckboxField.vue';
import InputField from '../forms/fields/InputField.vue';
import SelectField from '../forms/fields/SelectField.vue';
import TextareaField from '../forms/fields/TextareaField.vue';
import Label from '../forms/Label.vue';

import type { IClientQuoteRecipient } from 'shared/types';

const props = defineProps({
  isOpen: Boolean
});

const emit = defineEmits(['modal-close', 'modal-submit']);

const orderStore = useOrderStore();
const userStore = useUserStore();

const { order } = storeToRefs(orderStore);

const orderId = computed(() => orderStore.orderId);
const userEmail = computed(() => userStore.user?.details?.contact_email ?? '');
const forCallsign = computed(() =>
  orderStore?.order?.callsign ? `for ${orderStore?.order?.callsign}` : ''
);

const recipients = ref<IClientQuoteRecipient[]>([]);
const from = ref(userEmail.value);
const target = ref(null);
const subject = ref(
  `AML Fuel Release for ${order?.value?.callsign} ${order?.value?.fulfilment_datetime_str} ${order?.value?.tails?.[0]?.tail_number?.registration} ${order?.value?.location?.airport_details?.icao_code} ${order?.value?.aml_order_number}`
);
const clientNote = ref('');
const sendAmlFuelRelease = ref(false);
const sendSupplierFuelRelease = ref(true);
const errors = ref({
  recipients: '',
  from: ''
});

const hasErrors = computed(() => Object.values(errors.value).some(Boolean));

const { data: clientQuoteAddresses, isLoading: isLoadingRecipients } =
  useQueryClientQuoteAddresses(orderId);

const { data: clientDocuments, isLoading: isLoadingClientDocuments } =
  useQueryOrderClientDocuments(orderId);

const { mutate: sendFuelReleaseMutation, isPending: isSending } = useMutationSendFuelRelease();

const isLoading = computed(
  () => isSending.value || isLoadingClientDocuments.value || isLoadingRecipients.value
);

const mapRecipientDisplay = (recipient: IClientQuoteRecipient) => ({
  ...recipient,
  display: `${recipient.name} (${recipient.description})`
});

const recipientOptions = computed(
  () => clientQuoteAddresses?.value?.recipients?.map(mapRecipientDisplay) ?? []
);

const validate = () => {
  errors.value = {
    recipients: recipients.value?.length ? '' : 'Please select at least one recipient',
    from: from.value ? '' : 'Please select a sender'
  };
};

const onSend = async () => {
  validate();

  if (hasErrors.value) {
    return notify('Error while submitting, form is not valid!', 'error');
  } else {
    await sendFuelReleaseMutation(
      {
        orderId: orderId.value,
        payload: {
          recipients: recipients.value.map((recipient) => ({
            name: recipient.name,
            address: recipient.address,
            recipient_type: recipient.recipient_type
          })),
          sender: from.value,
          subject: subject.value,
          notes: clientNote.value,
          send_aml_fuel_release: sendAmlFuelRelease.value,
          send_supplier_fuel_release: sendSupplierFuelRelease.value
        }
      },
      {
        onSuccess: () => {
          notify('Sent successfully!', 'success');
          emit('modal-close');
          emit('modal-submit');
        }
      }
    );
  }
};

watch(clientQuoteAddresses, () => {
  if (clientQuoteAddresses.value?.recipients) {
    recipients.value = clientQuoteAddresses.value.recipients
      .filter((recipient) => recipient.is_pre_selected)
      .map(mapRecipientDisplay);
  }
});

watch(clientDocuments, () => {
  console.log('DOCS >>>', clientDocuments.value);
});
</script>

<style scoped lang="scss">
.form-body-wrapper {
  max-height: 500px;
}

.order-modal-footer {
  align-items: center;
  flex: 0 0 72px;
  min-height: 72px;

  .modal-button {
    max-height: 44px;
  }
}

.file-title {
  font-size: 15px;
  line-height: 24px;
  font-weight: 600;
}
</style>
