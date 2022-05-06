// Input Debounce: waiting for some time after last event before doing sth, for performance reasons, rate-limiting funcs, etc
const debounce = (func, delay = 1000) => {
  let timeoutId;
  return (...args) => {
    if (timeoutId) clearTimeout(timeoutId);
    timeoutId = setTimeout(() => {
      func.apply(null, args);
    }, delay);
  };
};
