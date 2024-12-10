def generate_group_project_query(full_path, after):
    return {
        'query': """
        query {
            group(fullPath:\"%s\") {
                    projects(after:\"%s\", includeSubgroups:true) {
                    nodes {
                        id,
                        name,
                        fullPath,
                        archived,
                        lastActivityAt,
                        webUrl,
                        namespace {
                            fullPath
                        }
                        statistics {
                            packagesSize,
                            repositorySize,
                            wikiSize,
                            lfsObjectsSize,
                            snippetsSize,
                            uploadsSize
                        }
                    }
                    pageInfo {
                        endCursor
                        hasNextPage
                    }
                }
            }
        }
        """ % (full_path, after)
    }

def generate_all_projects_query(after):
    return {
            'query': """
            query {
                projects(after:\"%s\") {
                    nodes {
                            id,
                            name,
                            fullPath,
                            archived,
                            lastActivityAt,
                            webUrl,
                            namespace {
                                fullPath
                            }
                            statistics {
                                packagesSize,
                            }
                        }
                        pageInfo {
                            endCursor
                            hasNextPage
                        }
                }
            }
            """ % after
        }