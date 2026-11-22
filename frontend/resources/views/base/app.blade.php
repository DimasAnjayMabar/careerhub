<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
    <title>Tracer Study & Career Navigation</title>
</head>

<body>
    <!-- Hamburger Menu -->
    @include('include.hamburger_menu')
    
    <div id="main_content" class="transition-all duration-300 ease-in-out">
        <!-- Navbar -->
        @include('include.navbar')

        <main class="pt-8 px-8">
            @yield('content')
        </main>
    </div>

</body>
</html>