type FirstPurchasePayload = {
  orderNumber: string;
  source: string;
};

const events: Array<Record<string, string>> = [];

export function trackFirstPurchaseSuccess(payload: FirstPurchasePayload) {
  const event = {
    funnel: "first_purchase",
    step: "checkout_success",
    converted: "true",
    orderNumber: payload.orderNumber,
    source: payload.source,
  };
  events.push(event);
  return event;
}

export function getTrackedFunnelEvents() {
  return [...events];
}
