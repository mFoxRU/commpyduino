# Commands reference

[TOC]

## Quick reference

| Command byte | Command                |           Parameters            | Returns | Description                              |
| :----------: | :--------------------- | :-----------------------------: | :-----: | ---------------------------------------- |
|    `0x21`    | Soft reset             |                —                |    —    | Soft reset the device                    |
|    `0x22`    | Get buffer size        |                —                | `Size`  | Get maximum message size                 |
|    `0x31`    | Set pin mode           |          `Pin`, `Mode`          |    —    | Set `Pin` to `Mode`                      |
|    `0x40`    | Digital read           |              `Pin`              | `Value` | Read `Value` on `Pin`                    |
|    `0x41`    | Digital write          |         `Pin`, `Value`          |    —    | Digital write `Value` to `Pin`           |
|    `0x42`    | Digital write timeout  |    `Pin`, `Value`, `Timeout`    |    —    | Digital write `Value` to `Pin`, and revert it back after `Timeout` |
|    `0x43`    | Digital write sequence | `Pin`, `Value`, `N`, `Timeouts` |    —    | Digital write `Value` to `Pin`, and flip it after each of `N` timeouts in `Timeouts` |
|    `0x50`    | Analog read            |              `Pin`              | `Value` | Read `Value` on `Pin`                    |
|    `0x51`    | Analog write           |         `Pin`, `Value`          |    —    | Analog write `Value` to `Pin`            |

## Commands

### Soft reset

|                  |      | Value  | Size (bytes) |
| ---------------- | :--: | :----: | :----------: |
| **Command byte** |      | `0x21` |      1       |
| **Parameters**   |  —   |        |              |
| **Returns**      |  —   |        |              |

Restart the device. Note that this is a software reset, so hardware state will remain unchanged.

### Get buffer size

|                  |          |  Value   | Size (bytes) |
| :--------------- | :------: | :------: | :----------: |
| **Command byte** |          |  `0x22`  |      1       |
| **Parameters**   |    —     |          |              |
| **Returns**      | **Size** | 5..65535 |      2       |

Returns a maximum message size that can be read by the board. Size does not include leading `STX` and closing `ETX`, as well as `ESC` characters that were added during escaping step (See protocol `Frame construction algorithm` step 5)

### Set pin mode

|                  |          |    Value    | Size (bytes) |
| :--------------- | :------: | :---------: | :----------: |
| **Command byte** |          |   `0x31`    |      1       |
| **Parameters**   | **Pin**  |             |      1       |
|                  | **Mode** | 0 \| 1 \| 2 |      1       |
| **Returns**      |    —     |             |              |

Sets `Pin` to `Mode`, where `Mode` is:

- `0`: Input
- `1`: Output
- `2` Input with internal pullup

### Digital read

|                  |           | Value  | Size (bytes) |
| :--------------- | :-------: | :----: | :----------: |
| **Command byte** |           | `0x40` |      1       |
| **Parameters**   |  **Pin**  |        |      1       |
| **Returns**      | **Value** | 0 \| 1 |      1       |

Read `Value` on `Pin`, where `Value` is

- `0`: Low
- `1`: High

### Digital write

|                  |           | Value  | Size (bytes) |
| :--------------- | :-------: | :----: | :----------: |
| **Command byte** |           | `0x41` |      1       |
| **Parameters**   |  **Pin**  |        |      1       |
|                  | **Value** | 0 \| 1 |      1       |
| **Returns**      |     —     |        |              |

Write `Value` to `Pin`, where `Value` is

- `0`: Low
- `1`: High

### Digital write timeout

|                  |             |  Value   | Size (bytes) |
| :--------------- | :---------: | :------: | :----------: |
| **Command byte** |             |  `0x42`  |      1       |
| **Parameters**   |   **Pin**   |          |      1       |
|                  |  **Value**  |  0 \| 1  |      1       |
|                  | **Timeout** | 0..65535 |      2       |
| **Returns**      |      —      |          |              |

Write `Value` to `Pin` and revert it back after `Timeout` ms. `Value` values are:

- `0`: Low
- `1`: High

### Digital write sequence

|                  |              |      Value       | Size (bytes) |
| :--------------- | :----------: | :--------------: | :----------: |
| **Command byte** |              |      `0x43`      |      1       |
| **Parameters**   |   **Pin**    |                  |      1       |
|                  |  **Value**   |      0 \| 1      |      1       |
|                  |    **N**     |      1..255      |      1       |
|                  | **Timeouts** | 0..65535 [, ...] |    2*`N`     |
| **Returns**      |      —       |                  |              |

Write `Value` to `Pin` and flip it after each of `N` timeout (ms) in `Timeouts`. `Value` values are:

- `0`: Low
- `1`: High

### Analog read

|                  |           |  Value  | Size (bytes) |
| :--------------- | :-------: | :-----: | :----------: |
| **Command byte** |           | `0x50`  |      1       |
| **Parameters**   |  **Pin**  |         |      1       |
| **Returns**      | **Value** | 0..1023 |      2       |

Read `Value` on `Pin`.

### Analog write

|                  |           | Value  | Size (bytes) |
| :--------------- | :-------: | :----: | :----------: |
| **Command byte** |           | `0x51` |      1       |
| **Parameters**   |  **Pin**  |        |      1       |
|                  | **Value** | 0..255 |      1       |
| **Returns**      |     —     |        |              |

Write `Value` to `Pin`.
