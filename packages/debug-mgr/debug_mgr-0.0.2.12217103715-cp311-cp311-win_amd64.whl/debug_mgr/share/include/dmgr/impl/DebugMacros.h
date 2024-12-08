
#ifndef INCLUDED_DEBUG_MACROS_H
#define INCLUDED_DEBUG_MACROS_H
#include <stdio.h>
#include "dmgr/IDebug.h"

#define DEBUG_INIT(scope, mgr) \
    if (!m_dbg) { \
        m_dbg = ((mgr))?(mgr)->findDebug(scope):0; \
    }
#define DEBUG_EN (m_dbg && m_dbg->en())
#define DEBUG_ENTER(fmt, ...) \
    if (m_dbg && m_dbg->en()) m_dbg->enter(fmt, ##__VA_ARGS__)
#define DEBUG_LEAVE(fmt, ...) \
    if (m_dbg && m_dbg->en()) m_dbg->leave(fmt, ##__VA_ARGS__)
#define DEBUG(fmt, ...) \
    if (m_dbg && m_dbg->en()) m_dbg->debug(fmt, ##__VA_ARGS__)
#define DEBUG_ERROR(fmt, ...) \
    if (m_dbg) m_dbg->error(fmt, ##__VA_ARGS__); else { \
        fprintf(stdout, "Error: "); \
        fprintf(stdout, fmt, ##__VA_ARGS__); \
        fprintf(stdout, "\n"); \
        fflush(stdout); }
#define DEBUG_FATAL(fmt, ...) \
    if (m_dbg) m_dbg->fatal(fmt, ##__VA_ARGS__)

#endif
