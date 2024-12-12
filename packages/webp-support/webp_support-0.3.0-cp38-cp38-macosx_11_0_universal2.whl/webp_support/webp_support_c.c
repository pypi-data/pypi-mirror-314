#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include <stdio.h>
#include <stdbool.h>

struct browser_version {
    const char *name;
    int min_version;
    size_t name_len;
};

static const struct browser_version browser_versions[] = {
    {"Firefox", 65, 7},
    {"Chrome", 32, 6},
    {"Edge", 18, 4},
    {"AppleWebKit", 605, 11},
    {"OPR", 19, 3},
    {"UCBrowser", 12, 9},
    {"SamsungBrowser", 4, 14},
    {"QQBrowser", 10, 9}
};

#define BROWSER_VERSION_COUNT (sizeof(browser_versions) / sizeof(browser_versions[0]))

bool is_webp_supported(const char *user_agent)
{
    if (user_agent == NULL)
    {
        return false;
    }

    const size_t count = BROWSER_VERSION_COUNT;
    
    for (size_t i = 0; i < count; i++)
    {
        const struct browser_version *current_browser = &browser_versions[i];
        const char *found = strstr(user_agent, current_browser->name);
        if (found != NULL)
        {
            const char *version = found + current_browser->name_len;
            while (!isdigit(*version) && *version != '\0')
            {
                version++;
            }
            if (*version != '\0')
            {
                int version_number = atoi(version);
                if (version_number >= current_browser->min_version)
                {
                    return true;
                }
            }
        }
    }

    return false;
}
