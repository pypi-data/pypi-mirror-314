/*
 * Copyright (C) 2023 Dominik Drexler and Simon Stahlberg
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program. If not, see <https://www.gnu.org/licenses/>.
 */

#ifndef MIMIR_SEARCH_ALGORITHMS_INTERFACE_HPP_
#define MIMIR_SEARCH_ALGORITHMS_INTERFACE_HPP_

#include "mimir/search/action.hpp"
#include "mimir/search/plan.hpp"
#include "mimir/search/state.hpp"

#include <optional>

namespace mimir
{

enum SearchStatus
{
    IN_PROGRESS,
    OUT_OF_TIME,
    OUT_OF_MEMORY,
    FAILED,
    EXHAUSTED,
    SOLVED,
    UNSOLVABLE
};

struct SearchResult
{
    SearchStatus status = SearchStatus::IN_PROGRESS;
    std::optional<Plan> plan = std::nullopt;
    std::optional<State> goal_state = std::nullopt;
};

/**
 * Interface class.
 */

class IAlgorithm
{
public:
    virtual ~IAlgorithm() = default;

    /// @brief Find a plan for the initial state.
    virtual SearchResult find_solution() = 0;

    /// @brief Find a plan for a given state.
    virtual SearchResult find_solution(State start_state) = 0;
};

}
#endif