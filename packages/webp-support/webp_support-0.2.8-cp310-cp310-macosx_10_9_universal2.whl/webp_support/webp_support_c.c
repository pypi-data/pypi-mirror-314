#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include <stdio.h>
#include <stdbool.h>
struct browser_version
{
    const char *name;
    int min_version;
};

static const struct browser_version browser_versions[] = {
    {"Firefox", 65},
    {"Chrome", 32},
    {"Edge", 18},
    {"AppleWebKit", 605},
    {"OPR", 19},
    {"UCBrowser", 12},
    {"SamsungBrowser", 4},
    {"QQBrowser", 10}};

#define BROWSER_VERSION_COUNT (sizeof(browser_versions) / sizeof(browser_versions[0]))

bool is_webp_supported(const char *user_agent)
{
    if (user_agent == NULL)
    {
        return false;
    }

    const char *found;
    const char *version;
    int version_number;
    for (size_t i = 0; i < BROWSER_VERSION_COUNT; i++)
    {
        found = strstr(user_agent, browser_versions[i].name);
        if (found != NULL)
        {
            version = found + strlen(browser_versions[i].name);
            while (!isdigit(*version) && *version != '\0')
            {
                version++;
            }
            if (*version != '\0')
            {
                version_number = atoi(version);
                if (version_number >= browser_versions[i].min_version)
                {
                    return true;
                }
            }
        }
    }

    return false;
}
