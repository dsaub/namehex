<script setup>
import { ref, computed } from 'vue'

const inputValue = ref('')
const appliedColor = ref('#2e2d2d')

const showError = computed(() => {
    return inputValue.value.length > 0 && !inputValue.value.startsWith('#')
})

function applyColor() {
    if (inputValue.value.startsWith('#')) {
        appliedColor.value = inputValue.value
    } else {
        appliedColor.value = '#2e2d2d'
    }
}
</script>

<template>
<header>
    <h1>Name a Hexadecimal Colour</h1>
    <button>Iniciar Sesión</button>
    <button>Registrarse</button>
</header>
<main>
    <div id="search">
        <div class="input-wrapper">
            <input type="text" v-model="inputValue" @blur="applyColor" placeholder="Introduzca un color..." :style="{ backgroundColor: appliedColor, color: appliedColor !== '#2e2d2d' ? '#000' : '#FEFEFE' }" />
        </div>
        <button>Buscar</button>
    </div>
    <p v-if="showError" class="error">El valor debe comenzar con #</p>
</main>
</template>

<style lang="scss" scoped>

header {
    display: flex;
    align-items: center;
    justify-content: center;
    button {
        margin-top: 1rem;
        margin-bottom: 1rem;
        margin-right: 1rem;
        padding: 0.5rem;
        border: none;
        border-radius: 10px;
        color: #FEFEFE;
        background-color: #2e2d2d;
    }
    h1 {
        color: #FEFEFE;
        justify-self: center;
        margin-right: auto;
    }
}
main {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    min-height: 100vh;

    #search {
        display: flex;

        & > * {
            margin-left: 0.5rem;
            margin-right: 0.5rem;
            background-color: #2e2d2d;
            color: #FEFEFE;
            border: none;
            padding: 1rem;
            border-radius: 10px;
        }

        .input-wrapper {
            padding: 2px;
            border-radius: 12px;
            background: none;

            &:focus-within {
                background: conic-gradient(from 0deg, #ff0000, #00ff00, #0000ff, #ff0000);
                animation: spin 2s linear infinite;
            }

            & > input {
                width: 300px;
                padding: calc(1rem - 2px);
                border-radius: 10px;
                border: none;
                outline: none;
                color: #FEFEFE;
                transition: background-color 0.3s ease;
            }
        }
    }

    .error {
        color: #ff4444;
        margin-top: 0.5rem;
    }
}

@keyframes spin {
    to {
        filter: hue-rotate(360deg);
    }
}




</style>