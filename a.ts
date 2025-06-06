import {
    BaseGraphQlResult,
    GraphqlFilter,
    GraphqlQueryVariables,
    RelatedSubscription,
    RelatedSubscriptionsResult,
    Subscription,
    PageInfo, // If you have this type defined
} from '@/types';

import { orchestratorApi } from '../api';

export const RelatedSubscriptionsQuery = `
query RelatedSubscriptions(
    $subscriptionId: String!
    $first: Int!
    $after: Int!
    $sortBy: [GraphqlSort!]
    $terminatedSubscriptionFilter: [GraphqlFilter!]
) {
    subscriptions(
        filterBy: { value: $subscriptionId, field: "subscriptionId" }
    ) {
        page {
            subscriptionId
            inUseBySubscriptions(
                first: $first
                after: $after
                sortBy: $sortBy
                filterBy: $terminatedSubscriptionFilter
            ) {
                page {
                    subscriptionId
                    customer {
                        fullname
                    }
                    description
                    insync
                    startDate
                    status
                    product {
                        tag
                    }
                }
                pageInfo {
                    endCursor
                    hasNextPage
                    hasPreviousPage
                    startCursor
                    totalItems
                    sortFields
                    filterFields
                }
            }
        }
    }
}
`;

export type RelatedSubscriptionsResponse = {
    relatedSubscriptions: RelatedSubscription[];
    pageInfo: PageInfo; // Make sure this is declared in your types
} & BaseGraphQlResult;

export type RelatedSubscriptionVariables =
    GraphqlQueryVariables<RelatedSubscription> &
    Pick<Subscription, 'subscriptionId'> & {
        terminatedSubscriptionFilter?: GraphqlFilter<RelatedSubscription>;
    };

const relatedSubscriptionsApi = orchestratorApi.injectEndpoints({
    endpoints: (build) => ({
        getRelatedSubscriptions: build.query<
            RelatedSubscriptionsResponse,
            RelatedSubscriptionVariables
        >({
            query: (variables) => ({
                document: RelatedSubscriptionsQuery,
                variables,
            }),
            transformResponse: (
                result: RelatedSubscriptionsResult
            ): RelatedSubscriptionsResponse => {
                const relatedSubscriptionResultForSubscription =
                    result.subscriptions?.page?.[0] || {};

                const relatedSubscriptions =
                    relatedSubscriptionResultForSubscription.inUseBySubscriptions?.page || [];

                const pageInfo =
                    relatedSubscriptionResultForSubscription.inUseBySubscriptions?.pageInfo || {
                        endCursor: null,
                        hasNextPage: false,
                        hasPreviousPage: false,
                        startCursor: null,
                        totalItems: 0,
                        sortFields: [],
                        filterFields: [],
                    };

                return {
                    relatedSubscriptions,
                    pageInfo,
                    success: true,
                    message: '', // fill in from result if needed
                };
            },
        }),
    }),
});

export const { useGetRelatedSubscriptionsQuery } = relatedSubscriptionsApi;
