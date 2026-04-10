import { defineStore } from "pinia";
import { ref } from "vue";

const useCookieStore = defineStore('cookie-store', () => {

    // State 
    const cookies = ref(false);
    const cookiesPopup = ref(true);

    // Actions
    const acceptCookies = () => {
        if (!cookies.value){
            cookies.value = true;
            cookiesPopup.value = false;
        }
        
    };

    return {
        cookies,
        cookiesPopup,
        acceptCookies
    }
})
export { useCookieStore}