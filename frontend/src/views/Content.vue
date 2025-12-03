<template>
    <main>
        <div class="container">
            <div class="hero">
                <h1>Добро пожаловать в BookHub</h1>
                <p>Платформа для любителей книг</p>
                <a @click="$router.push('/books')" class="btn">Начать чтение</a>
            </div>
            
            <div class="features">
                <div class="card feature-card">
                    <h3>Библиотека</h3>
                    <p>Коллекция книг различных жанров</p>
                </div>
                <div class="card feature-card">
                    <h3>Сообщество</h3>
                    <p>Общайтесь с другими читателями</p>
                </div>
                <div class="card feature-card">
                    <h3>Рекомендации</h3>
                    <p>Персональные подборки книг</p>
                </div>
            </div>
        </div>  
    </main>
</template>

<script setup></script>

<style scoped></style>
