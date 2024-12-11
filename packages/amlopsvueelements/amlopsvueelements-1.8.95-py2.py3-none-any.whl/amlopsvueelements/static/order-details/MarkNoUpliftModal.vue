<template>
  <div v-if="props.isOpen" class="order-modal">
    <div class="order-modal-wrapper">
      <div ref="target" class="order-modal-container">
        <div class="order-modal-body">
          <OrderForm add-default-classes is-modal>
            <template #header>
              <div class="header w-full flex justify-between">
                <div class="text-[1.25rem] font-medium text-grey-1000">Mark as No-Uplift</div>
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
                <SelectField
                  v-model="selectedOption"
                  :required="true"
                  label-text="Reason for No Uplift"
                  placeholder="Choose Reason"
                  label="name"
                  :options="noUpliftReasons ?? []"
                />
                <TextareaField v-model="body" class="w-full" label-text="Comment" placeholder="" />
                <div class="counter flex w-full justify-end">
                  {{ `${body.length} / ${MAX_COMMENT_LENGTH}` }}
                </div>
              </div>
            </template>
          </OrderForm>
        </div>
        <div class="order-modal-footer">
          <Loading v-if="isMarking" class="mr-4" />
          <button class="modal-button cancel" @click.stop="emit('modal-close')">Back</button>
          <button
            class="modal-button submit"
            :disabled="body.length > MAX_COMMENT_LENGTH || !selectedOption"
            @click.stop="onValidate()"
          >
            Confirm
          </button>
        </div>
      </div>
    </div>
    <ConfirmationModal
      :is-open="isConfirmModalOpen"
      title="Please confirm that you intend to confirm that no fuel uplift took place (this will close the order)"
      confirm-button="Yes"
      cancel-button="No"
      @modal-close="closeConfirmationModal"
      @modal-confirm="onSubmit"
    />
  </div>
</template>

<script lang="ts" setup>
import { computed, ref, shallowRef } from 'vue';
import { useQueryClient } from '@tanstack/vue-query';
import { useOrderStore } from '@/stores/useOrderStore';
import OrderForm from '@/components/forms/OrderForm.vue';
import { useMutationMarkAsNoUplift } from '@/services/mutations/uplift';
import { useQueryNoUpliftReasons } from '@/services/queries/uplift';
import { notify } from '@/helpers/toast';
import SelectField from '../forms/fields/SelectField.vue';
import TextareaField from '../forms/fields/TextareaField.vue';
import Loading from '../forms/Loading.vue';
import ConfirmationModal from './ConfirmationModal.vue';

import type { INoUpliftReason } from 'shared/types';

const props = defineProps({
  isOpen: Boolean
});

const emit = defineEmits(['modal-close', 'modal-submit']);

const MAX_COMMENT_LENGTH = 200;

const queryClient = useQueryClient();
const orderStore = useOrderStore();

const selectedOption = ref<INoUpliftReason>();
const target = ref(null);
const body = ref('');
const isConfirmModalOpen = shallowRef(false);

const orderId = computed(() => orderStore.orderId);
const isOpen = computed(() => props.isOpen);

const { data: noUpliftReasons } = useQueryNoUpliftReasons(orderId, {
  enabled: isOpen
});

const { mutate: markAsNoUpliftMutation, isPending: isMarking } = useMutationMarkAsNoUplift();

const closeConfirmationModal = () => {
  isConfirmModalOpen.value = false;
};

const onValidate = async () => {
  const isValid = body.value.length <= MAX_COMMENT_LENGTH && !!selectedOption.value;
  if (!isValid) {
    return notify('Error while submitting, form is not valid!', 'error');
  } else {
    isConfirmModalOpen.value = true;
  }
};

const onSubmit = async () => {
  isConfirmModalOpen.value = false;

  if (!selectedOption.value) return;

  await markAsNoUpliftMutation(
    {
      orderId: orderId.value,
      payload: {
        loss_reason_id: selectedOption.value.id,
        comments: body.value
      }
    },
    {
      onSuccess: () => {
        queryClient.invalidateQueries({ queryKey: ['orderStatus', orderId.value] });
        emit('modal-close');
        emit('modal-submit');
      }
    }
  );
};
</script>

<style scoped lang="scss">
.order-modal-footer {
  align-items: center;
  flex: 0 0 72px;
  min-height: 72px;

  .modal-button {
    max-height: 44px;
  }
}
</style>
