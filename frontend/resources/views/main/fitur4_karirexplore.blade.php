@extends('base.fitur4')

@section('karir-explore-content')

    @if ($error)
        <div class="text-red-500 text-center">
            {{ $error }}
        </div>
    @else
        <div class="flex flex-col mb-8 ">
            <h2 class="text-2xl font-semibold text-[#0F294A]">Browse Karir per Bidang</h2>
        </div>

        <!-- Dropdown Form -->
        <div class="mb-8">
            <form method="GET" action="/career-navigation">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <!-- Bidang 1 -->
                    <div>
                        <label for="bidang1"
                            class="block text-sm font-medium text-gray-600 mb-2">
                            Pilih Bidang 1
                        </label>

                        <div class="relative">
                            <select name="bidang1" id="bidang1" onchange="this.form.submit()" class="appearance-none w-full bg-gray-100 text-[#0F294A] px-4 py-2.5 rounded-lg border border-transparent cursor-pointer
                                hover:bg-gray-200/70 focus:outline-none focus:bg-white focus:border-[#2B72D6] focus:ring-2 focus:ring-[#2B72D6]/20">

                                <option value="">(tidak ada)</option>

                                @foreach ($bidangList as $b)
                                    <option value="{{ $b }}"
                                        @selected($b === $bidang1)>
                                        {{ $b }}
                                    </option>
                                @endforeach
                            </select>

                            <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-4 text-gray-600">
                                <svg class="h-4 w-4" fill="none" stroke="currentColor"stroke-width="2" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" />
                                </svg>
                            </div>
                        </div>
                    </div>

                    <!-- Bidang 2 -->
                    <div>
                        <label for="bidang2"
                            class="block text-sm font-medium text-gray-600 mb-2">
                            Pilih Bidang 2
                        </label>

                        <select name="bidang2" id="bidang2"onchange="this.form.submit()" class="appearance-none w-full bg-gray-100 text-[#0F294A] px-4 py-2.5 rounded-lg border border-transparent cursor-pointer
                            hover:bg-gray-200/70 focus:outline-none focus:bg-white focus:border-[#2B72D6] focus:ring-2 focus:ring-[#2B72D6]/20">

                            <option value="">(tidak ada)</option>

                            @foreach ($bidangList as $b)
                                @if ($b !== $bidang1)
                                    <option value="{{ $b }}"
                                        @selected($b === $bidang2)>
                                        {{ $b }}
                                    </option>
                                @endif
                            @endforeach
                        </select>
                    </div>
                </div>
            </form>
        </div>

        <!--  -->
        <!-- Perbandingan Bidang -->
        <div class="grid grid-cols-2 gap-8 mb-6">
            <!-- Bidang 1 -->
            <div class="min-w-0">
                <div class="flex gap-2">
                    <h3 class="text-xl items-center">💼</h3>
                    <span class="text-xl font-semibold text-[#0F294A] mb-5">
                        {{ $bidang1 }}
                    </span>
                </div>

                <!-- Hard Skills -->
                <div class="mb-6">
                    <h4 class="font-semibold text-[#0F294A] mb-4">Hard Skills Teratas</h4>

                    <div class="flex flex-wrap gap-2">
                        @forelse ($card1['hard'] ?? [] as $row)
                            <span class="px-3 py-2 bg-blue-50 text-[#0F294A] rounded-lg text-sm">
                                {{ $row['skill'] }}
                            </span>
                        @empty
                            <p class="text-sm text-gray-400">Belum ada data hard skills</p>
                        @endforelse
                    </div>
                </div>

                <!-- Soft Skills -->
                <div class="mb-6">
                    <h4 class="font-semibold text-[#0F294A] mb-4">Soft Skills Teratas</h4>

                    <div class="flex flex-wrap gap-2">
                        @forelse ($card1['soft'] ?? [] as $row)
                            <span class="px-3 py-2 bg-blue-50 text-[#0F294A] rounded-lg text-sm">
                                {{ $row['skill'] }}
                            </span>
                        @empty
                            <p class="text-sm text-gray-400">Belum ada data soft skills</p>
                        @endforelse
                    </div>
                </div>

                <!-- Sertifikasi -->
                <div class="mb-6">
                    <h4 class="font-semibold text-[#0F294A] mb-4">Sertifikasi Bermanfaat</h4>

                    <div class="flex flex-wrap gap-2">
                        @forelse ($card1['sertifikasi'] ?? [] as $row)
                            <span class="px-3 py-2 bg-blue-50 text-[#0F294A] rounded-lg text-sm">
                                {{ $row['sertifikasi'] }}
                            </span>
                        @empty
                            <p class="text-sm text-gray-400">Belum ada data sertifikasi</p>
                        @endforelse
                    </div>
                </div>
            </div>


            <!-- Bidang 2 -->
         

                <div class="min-w-0 lg:border-l lg:border-gray-200 lg:pl-8">
                    <div class="flex gap-2">
                        <h3 class="text-xl items-center">💼</h3>
                        <span class="text-xl font-semibold text-[#0F294A] mb-5">
                            {{ $bidang2 }}
                        </span>
                    </div>

                    <!-- Hard Skills -->
                    <div class="mb-6">
                        <h4 class="font-semibold text-[#0F294A] mb-3">Hard Skills Teratas</h4>

                        <div class="flex flex-wrap gap-2">
                            @forelse ($card2['hard'] ?? [] as $row)
                                <span class="px-3 py-2 bg-blue-50 text-[#0F294A] rounded-lg text-sm">
                                    {{ $row['skill'] }}
                                </span>
                            @empty
                                <p class="text-sm text-gray-400">Belum ada data hard skills</p>
                            @endforelse
                        </div>
                    </div>

                    <!-- Soft Skills -->
                    <div class="mb-6">
                        <h4 class="font-semibold text-[#0F294A] mb-3">Soft Skills Teratas</h4>

                        <div class="flex flex-wrap gap-2">
                            @forelse ($card2['soft'] ?? [] as $row)
                                <span class="px-3 py-2 bg-blue-50 text-[#0F294A] rounded-lg text-sm">
                                    {{ $row['skill'] }}
                                </span>
                            @empty
                                <p class="text-sm text-gray-400">Belum ada data soft skills</p>
                            @endforelse
                        </div>
                    </div>

                    <!-- Sertifikasi -->
                    <div class="mb-6">
                        <h4 class="font-semibold text-[#0F294A] mb-3">Sertifikasi Bermanfaat</h4>

                        <div class="flex flex-wrap gap-2">
                            @forelse ($card2['sertifikasi'] ?? [] as $row)
                                <span class="px-3 py-2 bg-blue-50 text-[#0F294A] rounded-lg text-sm">
                                    {{ $row['sertifikasi'] }}
                                </span>
                            @empty
                                <p class="text-sm text-gray-400">Belum ada data sertifikasi</p>

                            @endforelse
                        </div>
                    </div>
                </div>
            

        </div>

    @endif

@endsection