# Status codes

| Status    | Code   | Description              |
| --------- | ------ | ------------------------ |
| OK        | `0x00` | Everything ok            |
| REQ_ERR   | `0x01` | Could not send request   |
| NO_ACK    | `0x02` | Didn't receive ACK       |
| REPLY_ERR | `0x03` | Didn't receive reply     |
| LEN_ERR   | `0x04` | Reply has wrong length   |
| CRC_ERR   | `0x05` | Reply has wrong CRC      |
| ID_ERR    | `0x06` | Reply has wrong frame ID |

