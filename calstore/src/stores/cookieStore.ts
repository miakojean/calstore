// stores/cookieStore.ts
import { defineStore } from "pinia";
import { ref, computed } from "vue";

const STORAGE_KEY = 'cookies-consent';

export const useCookieStore = defineStore('cookie-store', () => {
    const getInitialConsent = (): boolean => {
        try {
        return localStorage.getItem(STORAGE_KEY) === 'true';
        } catch {
        return false;
        }
    };

    const isCookieConsentGiven = ref<boolean>(getInitialConsent());

    const consentGiven = computed(() => isCookieConsentGiven.value);

    const setCookieConsent = (consent: boolean = true) => {
        try {
        if (consent) {
            localStorage.setItem(STORAGE_KEY, 'true');
        } else {
            localStorage.removeItem(STORAGE_KEY);
        }
        isCookieConsentGiven.value = consent;
        } catch (e) {
        console.error('Erreur localStorage', e);
        }
    };

  const revokeConsent = () => setCookieConsent(false);

  return {
    isCookieConsentGiven,   // à exposer en lecture seule si besoin
    consentGiven,
    setCookieConsent,
    revokeConsent,
  };
});