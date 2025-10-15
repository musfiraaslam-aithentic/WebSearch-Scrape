# Query: Standard PC (Q35 + ICH9, 2009) QEMU

The QEMU Standard PC (Q35 + ICH9, 2009) emulates a modern PC architecture, offering several advancements over older QEMU machine types like the I440FX. This model is designed to provide better support for features such as PCI-E passthrough.

### Specifications

The key specifications of the QEMU Standard PC (Q35 + ICH9, 2009) machine model are centered around its emulation of the Intel Q35 chipset as the North Bridge and the ICH9 (I/O Controller Hub) as the South Bridge.

*   **Chipset:**
    *   **North Bridge:** Intel Q35
    *   **South Bridge:** Intel ICH9
*   **Bus Architecture:**
    *   **PCI Express (PCI-E):** The Q35 chipset provides a virtual PCI-E bus, which is a significant improvement over the PCI-only I440FX. This allows for better support of PCI-E passthrough.
    *   **PCI Bus:** In addition to PCI-E, a PCI bus is also present.
    *   **LPC Bus:** For SuperIO devices.
    *   **No ISA Bus:** Unlike older architectures, the ICH9 does not have an ISA bus. Devices typically found on the ISA bus in older emulations (like serial, parallel, and floppy controllers) are managed differently.
*   **Integrated Controllers (ICH9):**
    *   **AHCI Controller:** Integrated for Serial ATA (SATA) storage, offering modern disk interface capabilities.
    *   **USB Controller:** Integrated USB support.
    *   **Network Adapter:** Integrated network capabilities.
    *   **Audio Adapter:** Integrated audio support.
*   **BIOS:** Commonly uses SeaBIOS, with versions such as `SeaBIOS rel-1.12.1-0-ga5cab58e9a3f-prebuilt.qemu.org` being observed in benchmarks. UEFI firmware like OVMF (EFI Development Kit II) can also be used.
*   **Other Emulated Devices (General QEMU Capabilities, applicable to Q35/ICH9):**
    *   **Graphics Card:** Can emulate various graphics cards, including Cirrus CLGD 5446 PCI VGA, Standard-VGA with Bochs-VBE, and Red Hat QXL VGA.
    *   **Network Card:** Support for Realtek 8139C+ PCI, NE2000 PCI, PCnet, E1000 (PCI Intel Gigabit Ethernet), and E1000E (PCIe Intel Gigabit Ethernet).
    *   **Storage:** Besides AHCI for SATA, it supports NVMe disk interfaces and various disk image formats.
    *   **Input Devices:** PS/2 mouse and keyboard.
    *   **Peripherals:** Serial port, parallel port, PC speaker, and CD/DVD-ROM drive emulation.

### References (URLs)

1.  [https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHNkUekTK8XIhQ0LVm5zVPjfW8s_15T-i7EB0vXwJM9RU8i_V1XU0kW3oMtaeVnw57JyFf2-2CjtBcNX_Ji3kqvQlXCsLsXF7_nLidGIdq9IgTWNC03SCL7emX8qj7BbTnXqGutfDbMfAZ5sOrYXUQZbJbhxBiyrwQL7nEle9UvOasNEMvow8Bdtlen6x3v-JRa1jY=](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHNkUekTK8XIhQ0LVm5zVPjfW8s_15T-i7EB0vXwJM9RU8i_V1XU0kW3oMtaeVnw57JyFf2-2CjtBcNX_Ji3kqvQlXCsLsXF7_nLidGIdq9IgTWNC03SCL7emX8qj7BbTnXqGutfDbMfAZ5sOrYXUQZbJbhxBiyrwQL7nEle9UvOasNEMVowyBdtlen6x3v-JRa1jY=)
2.  [https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEjkVRFJBc_4e33TjwhGjUhH9o9me2bfxWRCEaVKxCwAtzUplaY4roC_T4IwZkm-jb1hU0wquYrH0z7VIEu6Xb28cmdNOvyUrlqZfrw1fWODBjNKJdUMO3LRh6EdWXEeBEKfouFx-u2bjL3odNSQTX](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEjkVRFJBc_4e33TjwhGjUhH9o9me2bfxWRCEaVKxCwAtzUplaY4roC_T4IwZkm-jb1hU0wquYrH0z7VIEu6Xb28cmdNOvyUrlqZfrw1fWODBjNKJdUMO3LRh6EdWXEeBEKfouFx-u2bjL3odNSQTX)
3.  [https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGK285fHJNnqkaZFU8h-YUrA9Bz3ttMU29KBoY5x4MPTpwK_hPIzl7VIm4bXAJnLhCgJmf2o-NlvLkCB2zVsSs651MtbozMnpsj3qts2ToMV1M7mRKDu5qwznRSta4=](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGK285fHJNnqkaZFU8h-YUrA9Bz3ttMU29KBoY5x4MPTpwK_hPIzl7VIm4bXAJnLhCgJmf2o-NlvLkCB2zVsSs651MtbozMnpsj3qts2ToMV1M7mRKDu5qwznRSta4=)
4.  [https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEHfIasexKiWHqNt8uV5ALQQ34AnzPrTNrgkEv2vEeHJj3vQ5FUqMNmGi3XhKbjn20UeNp0eDy2M-M3iDpATE_TLTgCPBKTcChoiZapBW86fD5k5I77w6EH5ytaZVpikcJoFfv9KW4DFZEV40alsJJk6HWuOHvV1Kc2-gWuAMSprw==](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEHfIasexKiWHqNt8uV5ALQQ34AnzPrTNrgkEv2vEeHJj3vQ5FUqMNmGi3XhKbjn20UeNp0eDy2M-M3iDpATE_TLTgCPBKTcChoiZapBW86fD5k5I77w6EH5ytaZVpikcJoFfv9KW4DFZEV40alsJJk6HWuAMSprw==)
5.  [https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFlw7W6QvolSkmJDksrRsjsCvU4lJR1vxLYu56BbmtMroobN92SssEYwWTTPI8fmMKZ22dlE72m1OEw-J6iurb96oz7ABD_vQXQa10soxcu9zhFTNtaDqVZplDBVD98U1NEK4VM2yrQohemnzqqegSapVyEIWBG88SUk2mbdsOAk0=](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFlw7W6QvolSkmJDksrRsjsCvU4lJR1vxLYu56BbmtMroobN92SssEYwWTTPI8fmMKZ22dlE72m1OEw-J6iurb96oz7ABD_vQXQa10soxcu9zhFTNtaDqVZplDBVD98U1NEK4VM2yrQohemnzqqegSapVyEIWBG88SUk2mbdsOAk0=)
6.  [https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGN39s39gdkxb_5auXeDQvLdN5LM8mPa0oBiKwly9GOjp66aqAaEtlSqTxYq7euwGeHW_PlvhcxwU8LUiwTBxnvcFVkLnX2yCsEDpdRdz0IaMj6BGQ3kkeQm7Gqb_qWxNGL4suLSB0=](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGN39s39gdkxb_5auXeDQvLdN5LM8mPa0oBiKwly9GOjp66aqAaEtlSqTxYq7euwGeHW_PlvhcxwU8LUiwTBxnvcFVkLnX2yCsEDpdRdz0IaMj6BGQ3kkeQm7Gqb_qWxNGL4suLSB0=)
7.  [https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQE9918-bd4eE3pEE28fx-leQmyAZ9vMhELFtHf_BbBqtZ9O-yPt88_3n0DbXF0dt_Xl1KF-pgM9fXaLhYGluXQW9jyLK10NE9qg5OZVzNIt9DAO9SiItEEPIsyM-EMa3QBOkF1vlOgTrGSY3astlTD_bx9CTqFY2ScRSTSyQFy4J1FDdi1ZezhxA36g3An5ZIQ=](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQE9918-bd4eE3pEE28fx-leQmyAZ9vMhELFtHf_BbBqtZ9O-yPt88_3n0DbXF0dt_Xl1KF-pgM9fXaLhYGluXQW9jyLK10NE9qg5OZVzNIt9DAO9SiItEEPIsyM-EMa3QBOkF1vlOgTrGSY3astlTD_bx9CTqFY2ScRSTSyQFy4J1FDdi1ZezhxA36g3An5ZIQ=)
8.  [https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEuCUO89ucpMntSTVYnWIyKwNkZlbeN7F8nIMO0TEgsOW1sZSAzUBXq9lh79BK3-KDgkOYR8a7G3T1S9QP9aWQb7ZjhYr4O4SN0wtbPwG3DXGlkBli9FpdRmhInzWQ=](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEuCUO89ucpMntSTVYnWIyKwNkZlbeN7F8nIMO0TEgsOW1sZSAzUBXq9lh79BK3-KDgkOYR8a7G3T1S9QP9aWQb7ZjhYr4O4SN0wtbPwG3DXGlkBli9FpdRmhInzWQ=)
9.  [https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHOwNo-5L8ggFeYeZkCHRFkwu_FdO369D1FmZPPq5iNKbNkUgAW5SSoLDGhhd-jUoqxn0YXjZ0CXtBYNJ5ZVSI3rvWgUWsKU9zgpEj22wbQJP2Ccbm2IMy0Fx6OD2VG3QJS2P3h](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHOwNo-5L8ggFeYeZkCHRFkwu_FdO369D1FmZPPq5iNKbNkUgAW5SSoLDGhhd-jUoqxn0YXjZ0CXtBYNJ5ZVSI3rvWgUWsKU9zgpEj22wbQJP2Ccbm2IMy0Fx6OD2VG3QJS2P3h)