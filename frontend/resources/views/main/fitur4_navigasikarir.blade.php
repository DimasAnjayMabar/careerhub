@extends('base.fitur4')

@section('navigasi-karir-content')

    <div class="mb-8">
        <h2 class="text-2xl font-semibold text-[#0F294A]">Ayo Navigasi Karirmu!</h2>
        <p class="text-sm text-gray-500 mt-4">
            Centang skill yang kamu miliki, sistem akan merekomendasikan
            bidang karier paling cocok berdasarkan pola alumni</p>
    </div>

    <!-- Form Career Matcher -->
    <form method="POST" action="/career-navigation/match">
        @csrf
        <div class="w-full bg-white border border-gray-200 rounded-xl p-6" data-picker-container>
            <div class="flex items-center gap-2.5 mb-6">
                <svg class="w-6 h-6 shrink-0" fill="none" stroke="#0F294A" stroke-width="2" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-4.35-4.35m1.85-5.15a7 7 0 1 1-14 0 7 7 0 0 1 14 0Z" />
                </svg>

                <span class="text-[#0F294A] text-lg font-semibold">
                    Mulai Career Matcher
                </span>
            </div>


            <!-- Hard Skills -->
            <div class="mb-8" data-skill-picker>
                <h4 class="font-semibold text-[#0F294A] mb-4">Hard Skills yang Kamu Miliki</h4>
                <div class="relative">
                    <button type="button"
                        data-picker-toggle
                        aria-expanded="false"
                        aria-controls="hard-skill-options"
                        class="flex w-full items-center gap-4 rounded-lg border border-gray-200 bg-white px-4 py-3 text-left
                            hover:border-[#2B72D6] focus:outline-none focus:ring-2 focus:ring-[#2B72D6]/20 transition">

                        <span data-picker-placeholder class="flex-1 text-sm text-gray-500">
                            Cari dan pilih hard skills...
                        </span>

                        <span data-selected-count class="shrink-0 rounded-full bg-gray-100 px-2 py-1 text-xs font-medium text-gray-600">
                            0 dipilih
                        </span>

                        <svg class="h-4 w-4 shrink-0 text-gray-500 transition-transform" data-picker-chevron
                            fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" d="m6 9 6 6 6-6" />
                        </svg>
                    </button>

                    <div id="hard-skill-options" data-picker-panel
                        class="absolute left-0 right-0 top-full z-30 mt-2 hidden overflow-hidden rounded-xl border border-gray-200 bg-white shadow-lg">

                        <div class="border-b border-gray-100 p-3">
                            <div class="relative">
                                <svg class="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400"
                                    fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                                    <circle cx="11" cy="11" r="7" />
                                    <path stroke-linecap="round" d="m16 16 4 4" />
                                </svg>
                                <input type="search"
                                    data-skill-search
                                    autocomplete="off"
                                    placeholder="Cari hard skills..."
                                    class="w-full rounded-lg border border-gray-200 py-2 pl-9 pr-3 text-sm text-[#0F294A]
                                        placeholder:text-gray-400 focus:border-[#2B72D6] focus:outline-none focus:ring-2 focus:ring-[#2B72D6]/20">
                            </div>
                        </div>

                        <div data-skill-options class="max-h-64 overflow-y-auto p-2">
                            @forelse ($hardSkills as $skill)
                                <label data-skill-option
                                    data-skill-name="{{ $skill['nama_skill'] }}"
                                    class="flex cursor-pointer items-center gap-3 rounded-lg px-3 py-2.5 text-sm text-[#0F294A]
                                        hover:bg-blue-50 transition">

                                    <input type="checkbox"
                                        data-skill-checkbox
                                        name="skill_ids[]"
                                        value="{{ $skill['skill_id'] }}"
                                        @checked(in_array((int) $skill['skill_id'], array_map('intval', $skillDipilih ?? []), true))
                                        class="h-4 w-4 rounded accent-[#2B72D6]">

                                    <span data-skill-label>{{ $skill['nama_skill'] }}</span>
                                </label>
                            @empty
                                <p class="px-3 py-2 text-sm text-gray-400">
                                    Belum ada pilihan hard skills.
                                </p>
                            @endforelse
                        </div>

                        <p data-no-results hidden class="border-t border-gray-100 px-4 py-3 text-sm text-gray-400">
                            Skill tidak ditemukan
                        </p>
                    </div>
                </div>

                <div data-selected-chips class="mt-3 flex flex-wrap gap-2" aria-live="polite"></div>
            </div>


            <!-- Soft Skills -->
            <div class="mb-8" data-skill-picker>
                <h4 class="font-semibold text-[#0F294A] mb-4">Soft Skills yang Kamu Miliki</h4>
                <div class="relative">
                    <button type="button"
                        data-picker-toggle
                        aria-expanded="false"
                        aria-controls="soft-skill-options"
                        class="flex w-full items-center gap-3 rounded-lg border border-gray-200 bg-white px-4 py-3 text-left
                            hover:border-[#2B72D6] focus:outline-none focus:ring-2 focus:ring-[#2B72D6]/20 transition">

                        <span data-picker-placeholder class="flex-1 text-sm text-gray-500">
                            Cari dan pilih soft skills...
                        </span>

                        <span data-selected-count class="shrink-0 rounded-full bg-gray-100 px-2 py-1 text-xs font-medium text-gray-600">
                            0 dipilih
                        </span>

                        <svg class="h-4 w-4 shrink-0 text-gray-500 transition-transform" data-picker-chevron
                            fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" d="m6 9 6 6 6-6" />
                        </svg>
                    </button>

                    <div id="soft-skill-options" data-picker-panel
                        class="absolute left-0 right-0 top-full z-30 mt-2 hidden overflow-hidden rounded-xl border border-gray-200 bg-white shadow-lg">

                        <div class="border-b border-gray-100 p-3">
                            <div class="relative">
                                <svg class="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400"
                                    fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                                    <circle cx="11" cy="11" r="7" />
                                    <path stroke-linecap="round" d="m16 16 4 4" />
                                </svg>
                                <input type="search"
                                    data-skill-search
                                    autocomplete="off"
                                    placeholder="Cari soft skills..."
                                    class="w-full rounded-lg border border-gray-200 py-2 pl-9 pr-3 text-sm text-[#0F294A]
                                        placeholder:text-gray-400 focus:border-[#2B72D6] focus:outline-none focus:ring-2 focus:ring-[#2B72D6]/20">
                            </div>
                        </div>

                        <div data-skill-options class="max-h-64 overflow-y-auto p-2">
                            @forelse ($softSkills as $skill)
                                <label data-skill-option
                                    data-skill-name="{{ $skill['nama_skill'] }}"
                                    class="flex cursor-pointer items-center gap-3 rounded-lg px-3 py-2.5 text-sm text-[#0F294A]
                                        hover:bg-blue-50 transition">

                                    <input type="checkbox"
                                        data-skill-checkbox
                                        name="skill_ids[]"
                                        value="{{ $skill['skill_id'] }}"
                                        @checked(in_array((int) $skill['skill_id'], array_map('intval', $skillDipilih ?? []), true))
                                        class="h-4 w-4 rounded accent-[#2B72D6]">

                                    <span data-skill-label>{{ $skill['nama_skill'] }}</span>
                                </label>
                            @empty
                                <p class="px-3 py-2 text-sm text-gray-400">
                                    Belum ada pilihan soft skills
                                </p>
                            @endforelse
                        </div>

                        <p data-no-results hidden class="border-t border-gray-100 px-4 py-3 text-sm text-gray-400">
                            Skill tidak ditemukan
                        </p>
                    </div>
                </div>

                <div data-selected-chips class="mt-3 flex flex-wrap gap-2" aria-live="polite"></div>
            </div>


            <!-- Validasi -->
            @if ($errors->any())

                <div class="bg-red-50 border border-red-200 text-red-600 rounded-lg p-3 mb-5 text-sm">
                    {{ $errors->first() }}
                </div>

            @endif


            <!-- Error Backend -->
            @if ($matchError)

                <div class="bg-red-50 border border-red-200 text-red-600 rounded-lg p-3 mb-5 text-sm">
                    {{ $matchError }}
                </div>

            @endif


            <!-- Tombol -->
            <button type="submit"
                class="bg-[#febb3d] hover:bg-[#E5A52F] text-white px-5 py-3 rounded-lg font-medium transition">
                Hitung Rekomendasi Karier 🚀
            </button>

        </div>

    </form>


    <!--  -->
    <!-- HASIL REKOMENDASI -->

    @if (!empty($hasil))

        <div class="mt-12 mb-6">
            <h3 class="text-xl font-semibold text-[#0F294A] mb-4">Hasil Rekomendasi Karier</h3>

            @if (!empty($meta['catatan']))
                <p class="text-sm text-gray-500 mb-6">
                    {{ $meta['catatan'] }}
                </p>

            @endif
            <div class="space-y-5">

                @foreach ($hasil as $i => $row)
                    <div class="bg-white border border-gray-200 rounded-xl p-5">
                        <!-- Nama Bidang dan Skor -->
                        <div class="flex flex-wrap items-center justify-between gap-4 mb-6">
                            <div>
                                <p class="text-xs text-gray-500 mb-1">
                                    Rekomendasi #{{ $i + 1 }}
                                </p>

                                <h4 class="text-lg font-semibold text-[#0F294A]">
                                    {{ $row['nama_bidang'] }}
                                </h4>
                            </div>

                            <div class="text-right">
                                <p class="text-sm text-gray-500">
                                    Skor Kecocokan
                                </p>
                                <span class="text-2xl font-bold text-[#2B72D6]">
                                    {{ number_format(($row['skor'] ?? 0) * 100, 1) }}%
                                </span>
                            </div>
                        </div>

                        <!-- Skill Match -->
                        <div class="mb-6">
                            <h5 class="font-semibold text-green-700 mb-3">
                                Skill yang Cocok
                            </h5>

                            <div class="flex flex-wrap gap-2">

                                @forelse ($row['match'] ?? [] as $skill)

                                    <span class="px-3 py-2 rounded-lg bg-green-100 text-green-700 text-sm">
                                        {{ $skill['nama_skill'] }}

                                        <span class="text-xs opacity-80">
                                            ({{ ucfirst($skill['jenis']) }})
                                        </span>
                                    </span>

                                @empty
                                    <p class="text-sm text-gray-400">
                                        Belum ada skill yang cocok
                                    </p>
                                @endforelse
                            </div>
                        </div>

                        <!-- Skill Gap -->
                        <div>
                            <h5 class="font-semibold text-orange-600 mb-3">
                                Skill yang Belum Dimiliki
                            </h5>
                            <div class="flex flex-wrap gap-2">

                                @forelse ($row['gap'] ?? [] as $skill)

                                    <span class="px-3 py-2 rounded-lg bg-orange-100 text-orange-700 text-sm">
                                        {{ $skill['nama_skill'] }}

                                        <span class="text-xs opacity-80">
                                            ({{ ucfirst($skill['jenis']) }})
                                        </span>
                                    </span>

                                @empty
                                    <p class="text-sm text-gray-400">
                                        Tidak ada skill gap
                                    </p>
                                @endforelse
                            </div>
                        </div>
                    </div>
                @endforeach
            </div>
        </div>

    @elseif (!empty($hasMatchResult) && !$matchError)

        <div class="mt-8 text-center text-gray-500">
            Tidak ada rekomendasi karier yang dapat ditampilkan
        </div>

    @endif


    
    <!-- INSIGHT SKILL PALING DICARI -->
    <!-- ================================================= -->

    <!-- @if (!empty($insight))

        <div class="mt-12 mb-8">

            <h3 class="text-xl font-semibold text-[#0F294A] mb-5">
                Insight Skill yang Paling Sering Dipilih
            </h3>

            <div class="overflow-x-auto rounded-lg border border-gray-200">

                <table class="min-w-full text-sm">

                    <thead class="bg-[#1E3A8A] text-white text-left">

                        <tr>
                            <th class="px-4 py-3 w-20 text-center">No</th>
                            <th class="px-4 py-3">Skill</th>
                            <th class="px-4 py-3 text-center">
                                Jumlah Dipilih
                            </th>
                        </tr>

                    </thead>

                    <tbody class="divide-y divide-gray-200">

                        @foreach ($insight as $i => $row)

                            <tr class="hover:bg-[#2B72D6]/5 transition">

                                <td class="px-4 py-3 text-center text-gray-600">
                                    {{ $i + 1 }}
                                </td>

                                <td class="px-4 py-3 font-medium text-[#0F294A]">
                                    {{ $row['skill'] }}
                                </td>

                                <td class="px-4 py-3 text-center">
                                    {{ $row['jumlah'] }}
                                </td>

                            </tr>

                        @endforeach

                    </tbody>

                </table>

            </div> -->

        </div>

    @endif


    <script>
        document.addEventListener('DOMContentLoaded', function () {
            const pickers = Array.from(document.querySelectorAll('[data-skill-picker]'));
            const pickerContainer = document.querySelector('[data-picker-container]');
            const basePaddingBottom = pickerContainer
                ? (parseFloat(window.getComputedStyle(pickerContainer).paddingBottom) || 0)
                : 0;

            // Menambah ruang di bawah card saat buka dropdown
            function updatePickerContainerSpacing() {
                if (!pickerContainer) return;

                // Kembalikan padding dasar sebelum menghitung kebutuhan ruang terbaru.
                pickerContainer.style.paddingBottom = basePaddingBottom + 'px';

                const openPanel = pickers
                    .map(function (item) {
                        return item.querySelector('[data-picker-panel]');
                    })
                    .find(function (item) {
                        return item && !item.classList.contains('hidden');
                    });

                if (!openPanel) return;

                const panelBottom = openPanel.getBoundingClientRect().bottom;
                const containerBottom = pickerContainer.getBoundingClientRect().bottom;
                const bottomGap = 20;
                const extraSpace = Math.max(0, panelBottom + bottomGap - containerBottom);

                pickerContainer.style.paddingBottom = (basePaddingBottom + extraSpace) + 'px';
            }

            pickers.forEach(function (picker) {
                const toggle = picker.querySelector('[data-picker-toggle]');
                const panel = picker.querySelector('[data-picker-panel]');
                const search = picker.querySelector('[data-skill-search]');
                const count = picker.querySelector('[data-selected-count]');
                const placeholder = picker.querySelector('[data-picker-placeholder]');
                const chips = picker.querySelector('[data-selected-chips]');
                const noResults = picker.querySelector('[data-no-results]');
                const chevron = picker.querySelector('[data-picker-chevron]');
                const options = Array.from(picker.querySelectorAll('[data-skill-option]'));
                const checkboxes = Array.from(picker.querySelectorAll('[data-skill-checkbox]'));

                const defaultPlaceholder = placeholder.textContent.trim();
                const addMorePlaceholder = defaultPlaceholder.replace('Cari dan pilih', 'Tambah atau cari');

                function closePicker() {
                    panel.classList.add('hidden');
                    toggle.setAttribute('aria-expanded', 'false');
                    chevron.classList.remove('rotate-180');
                    requestAnimationFrame(updatePickerContainerSpacing);
                }

                function openPicker() {
                    // Tutup dropdown lain agar halaman tetap rapi.
                    pickers.forEach(function (otherPicker) {
                        if (otherPicker !== picker) {
                            const otherPanel = otherPicker.querySelector('[data-picker-panel]');
                            const otherToggle = otherPicker.querySelector('[data-picker-toggle]');
                            const otherChevron = otherPicker.querySelector('[data-picker-chevron]');
                            otherPanel.classList.add('hidden');
                            otherToggle.setAttribute('aria-expanded', 'false');
                            otherChevron.classList.remove('rotate-180');
                        }
                    });

                    panel.classList.remove('hidden');
                    toggle.setAttribute('aria-expanded', 'true');
                    chevron.classList.add('rotate-180');
                    requestAnimationFrame(updatePickerContainerSpacing);
                    search.focus();
                }

                function updateSelectedSkills() {
                    const selected = checkboxes.filter(function (checkbox) {
                        return checkbox.checked;
                    });

                    count.textContent = selected.length + ' dipilih';
                    placeholder.textContent = selected.length > 0
                        ? addMorePlaceholder
                        : defaultPlaceholder;

                    chips.replaceChildren();

                    selected.forEach(function (checkbox) {
                        const option = checkbox.closest('[data-skill-option]');
                        const skillName = option.querySelector('[data-skill-label]').textContent.trim();

                        const chip = document.createElement('span');
                        chip.className = 'inline-flex items-center gap-2 rounded-full bg-blue-50 px-3 py-1.5 text-sm text-[#0F294A]';

                        const name = document.createElement('span');
                        name.textContent = skillName;

                        const removeButton = document.createElement('button');
                        removeButton.type = 'button';
                        removeButton.textContent = '×';
                        removeButton.setAttribute('aria-label', 'Hapus ' + skillName);
                        removeButton.className = 'text-base leading-none text-gray-500 hover:text-red-600';
                        removeButton.addEventListener('click', function () {
                            checkbox.checked = false;
                            updateSelectedSkills();
                        });

                        chip.append(name, removeButton);
                        chips.appendChild(chip);
                    });
                }

                function filterSkills() {
                    const keyword = search.value.trim().toLocaleLowerCase('id-ID');
                    let visibleCount = 0;

                    options.forEach(function (option) {
                        const skillName = option.dataset.skillName.toLocaleLowerCase('id-ID');
                        const isVisible = skillName.includes(keyword);
                        option.classList.toggle('hidden', !isVisible);

                        if (isVisible) {
                            visibleCount++;
                        }
                    });

                    noResults.hidden = options.length === 0 || visibleCount > 0;
                    requestAnimationFrame(updatePickerContainerSpacing);
                }

                toggle.addEventListener('click', function () {
                    const isOpen = toggle.getAttribute('aria-expanded') === 'true';

                    if (isOpen) {
                        closePicker();
                    } else {
                        openPicker();
                    }
                });

                search.addEventListener('input', filterSkills);

                checkboxes.forEach(function (checkbox) {
                    checkbox.addEventListener('change', updateSelectedSkills);
                });

                document.addEventListener('click', function (event) {
                    if (!picker.contains(event.target)) {
                        closePicker();
                    }
                });

                picker.addEventListener('keydown', function (event) {
                    if (event.key === 'Escape') {
                        closePicker();
                        toggle.focus();
                    }
                });

                // Menampilkan kembali pilihan sebelumnya setelah hasil match dikirim.
                updateSelectedSkills();
                filterSkills();
            });

            window.addEventListener('resize', updatePickerContainerSpacing);
        });
    </script>


@endsection