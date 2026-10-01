# Transcript: Jetson Orin Nano Hardware Assembly, QSPI Firmware Capsule Upgrade & Direct NVMe Boot Provisioning

- **Session Date**: `2026-10-01`
- **Focus**: NVIDIA Jetson Orin Nano Developer Kit (8GB) Hardware Provisioning, JetPack 7.2.1 (L4T r39.2.1) UEFI Capsule Upgrade, 512GB PCIe Gen4 NVMe Direct Boot, Network Setup & Headless OpenSSH Server Configuration.
- **Participants**: Aaradhya (User), Antigravity (Assistant)
- **Repository**: `brainstorm` (`F:\Aaradhya-Dev-Tamrakar\brainstorm`)
- **Epistemic Classification**: `EMPIRICALLY_VERIFIED` (Hardware ground truth, 59 photos, live SSH verification)

---

## 1. Context & Architectural Overview

The goal of this session was to execute complete zero-drift physical setup and operating system provisioning for a brand-new NVIDIA Jetson Orin Nano Developer Kit (8GB), bypassing slow microSD execution by writing the root filesystem directly to a high-speed Western Digital PC SN5000S 512GB PCIe Gen4 NVMe SSD with default 25W Super Mode.

### Key Hardware Coordinates
- **Board**: NVIDIA Jetson Orin Nano Developer Kit 8GB (`P/N: 945-13766-0000-000`, `S/N: 1423925603897`)
- **Storage**: WD PC SN5000S 512GB M.2 2280 PCIe Gen4 NVMe SSD (`/dev/nvme0n1`)
- **Firmware Path**: Factory `36.04.03` -> JetPack 7.2.1 `39.02.01` (`39.2.1-gcid-46758480`, ESRT `0x270201`)
- **Operating System**: Ubuntu 24.04.5 LTS (`GNU/Linux 6.8.12-1021-tegra aarch64`)
- **Active Network Target**:
  - Ethernet: `192.168.1.125` (`enP8p1s0`)
  - Wi-Fi: `192.168.1.126` (`wlP1p1s0`, `KEC Makerspace-5`)
  - SSH User: `kecmakerspace`

---

## 2. Chronological Milestones & Dialogue Transcript

### Phase 1: Hardware Audit & Connection
- **User**: Connects power (19V DC brick), DisplayPort cable to Dell monitor, Gigabit Ethernet, ViewSonic USB keyboard, and mouse.
- **Assistant**: Confirmed green power LED, active PWM cooling fan, and UEFI splash screen loading (`36.4.3-gcid-38968081`).
- **Evidence**: [`research/media/2026-10-01_jetson_orin_nano_setup/01_nvme_ssd_and_wifi_bottom_view.jpg`](file:///f:/Aaradhya-Dev-Tamrakar/brainstorm/research/media/2026-10-01_jetson_orin_nano_setup/01_nvme_ssd_and_wifi_bottom_view.jpg) to `09_uefi_boot_menu_prompt.jpg`.

### Phase 2: Jetson ISO Acquisition & SD Card Flashing
- **Action**: Downloaded `jetsoninstaller-r39.2.1-*.iso` (5.04 GB arm64) from NVIDIA Developer portal.
- **Flashing Tool**: BalenaEtcher on Windows 11 writing to 128GB ADATA MicroSD card.
- **Result**: Flashing & verification completed successfully at 14.7 MB/s.
- **Evidence**: Photos `10_nvidia_docs_and_iso_download.png` through `16_windows_explorer_sd_card_ejected.png`.

### Phase 3: QSPI Firmware Capsule Update (JetPack 7.2.1 / r39.2.1)
- **Prompt**: ISO boot menu detected outdated QSPI firmware (`36.04.03`) vs ISO firmware (`39.02.01`).
- **Execution**: User pressed `[Y]` to confirm capsule flash.
- **Stages**:
  - Stage 1: Capsule writing progress `5%...100%` -> auto-reboot.
  - Stage 2: PreIsoInstaller logic executed on UEFI `39.2.1-gcid-46758480` -> Secondary capsule update `7%...100%`.
- **Evidence**: Photos `17_qspi_firmware_update_prompt.jpg` to `29_grub_post_firmware_update_closeup.jpg`.

### Phase 4: Direct NVMe Target Installation
- **Selection**: User selected `*Install on NVMe` in GNU GRUB 2.12.
- **Detection**: Linux kernel enumerated PCIe Gen4 link at 31.5 Gb/s and identified `Orin Nano DevKit Super`.
- **Storage Layout**: Curtin/Subiquity formatted `/dev/nvme0n1p1` as 475.4 GB rootfs partition alongside 14 system/firmware slots.
- **Packages**: Installed `nvidia-container-toolkit`, `docker.io`, `nvidia-l4t-kernel`, and GNOME desktop stack.
- **Evidence**: Photos `30_installer_target_storage_install_on_nvme.jpg` to `44_l4tlauncher_attempting_direct_nvme_boot.jpg`.

### Phase 5: GUI Out-of-Box-Experience (OOBE)
- **Language & EULA**: English (US), accepted NVIDIA Embedded Software License.
- **Networking**: Connected to `KEC Makerspace-5` Wi-Fi.
- **Location**: Timezone configured to `Kathmandu, Nepal (+0545)`.
- **Credentials**: User account `kecmakerspace` created. Telemetry opted-out.
- **Result**: Desktop loaded with default **25W Super Mode** active in top panel.
- **Evidence**: Photos `45_ubuntu_desktop_gui_welcome_screen.jpg` to `57_jetson_orin_nano_desktop_wallpaper_25w_mode_active.jpg`.

### Phase 6: Network Audit & Headless OpenSSH Server Setup
- **User Action**: Ran `ip -br a` on terminal (Photo 58).
- **SSH Issue**: Initial SSH connection from Windows PC returned `Connection refused`.
- **Investigation**: Photo 59 confirmed `openssh-server` was installed but `ssh.service` was disabled / inactive in Ubuntu 24.04 socket mode.
- **Resolution**: Ran `sudo systemctl enable --now ssh` on the Jetson.
- **Final Verification**: Successfully authenticated and logged in via Windows PowerShell:
  ```powershell
  ssh kecmakerspace@192.168.1.125
  ```
  Kernel: `6.8.12-1021-tegra aarch64`, Ubuntu `24.04.5 LTS`.

---

## 3. Associated Artifacts & Evidence Files

1. **Comprehensive Runbook**: [`research/notes/2026-10-01_JETSON_ORIN_NANO_SETUP_AND_PROVISIONING_RUNBOOK.md`](file:///f:/Aaradhya-Dev-Tamrakar/brainstorm/research/notes/2026-10-01_JETSON_ORIN_NANO_SETUP_AND_PROVISIONING_RUNBOOK.md)
2. **Media Gallery**: [`research/media/2026-10-01_jetson_orin_nano_setup/`](file:///f:/Aaradhya-Dev-Tamrakar/brainstorm/research/media/2026-10-01_jetson_orin_nano_setup/) (59 images)
3. **Repository Sync Commit**: [`3c1efa5`](https://github.com/Aaradhya-Dev-Tamrakar/brainstorm/commit/3c1efa5)
