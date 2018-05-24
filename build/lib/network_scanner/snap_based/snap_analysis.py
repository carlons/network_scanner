# import snap
# graphfile = 'en-yagoFacts-d-r-id-pair.txt'
# prefix = 'yago-en'
# G =  snap.LoadEdgeList(snap.PNGraph, graphfile, 0, 1)
#
# # Print graph information
# snap.PrintInfo(G, prefix + ' article graph', prefix + '-article-graph-info.txt', True)
#
# # Node degree
# print 'Node degree...'
# inDegV = snap.TIntPrV()
# snap.GetNodeInDegV(G, inDegV)
# indegreeFile = open(prefix + '-article-id-indegree.txt', 'w')
# for item in inDegV:
#     indegreeFile.write(str(item.GetVal1()))
#     indegreeFile.write('\t')
#     indegreeFile.write(str(item.GetVal2()))
#     indegreeFile.write('\n')
#
# indegreeFile.close()
#
# outDegV = snap.TIntPrV()
# snap.GetNodeOutDegV(G, outDegV)
# outdegreeFile = open(prefix + '-article-id-outdegree.txt', 'w')
# for item in outDegV:
#     outdegreeFile.write(str(item.GetVal1()))
#     outdegreeFile.write('\t')
#     outdegreeFile.write(str(item.GetVal2()))
#     outdegreeFile.write('\n')
#
# outdegreeFile.close()
#
# # Plot
# print 'plot...'
# snap.PlotSccDistr(G, prefix + "-article-scc-distr", prefix + " article scc distribution")
# snap.PlotWccDistr(G, prefix + "-article-wcc-distr", prefix + " article wcc distribution")
# snap.PlotInDegDistr(G, prefix + "-article-indegree-distr", prefix + " article indegree distribution")
# snap.PlotOutDegDistr(G, prefix + "-article-outdegree-distr", prefix + " article outdegree distribution")
#
# # scc wcc
# print 'scc wcc...'
# sccDist = snap.TIntPrV()
# snap.GetSccSzCnt(G, sccDist)
# scc = open(prefix + '-article-scc-sz-cnt.txt', 'w')
# for item in sccDist:
#     scc.write(str(item.GetVal1()))
#     scc.write('\t')
#     scc.write(str(item.GetVal2()))
#     scc.write('\n')
#
# scc.close()
#
# mxscc = snap.GetMxScc(G)
# mxsccFile = open(prefix + '-article-mxscc.txt', 'w')
# for item in mxscc.Edges():
#     mxsccFile.write(str(item.GetSrcNId()))
#     mxsccFile.write('\t')
#     mxsccFile.write(str(item.GetDstNId()))
#     mxsccFile.write('\n')
#
# mxsccFile.close()
#
#
# wccDist = snap.TIntPrV()
# snap.GetWccSzCnt(G, wccDist)
# wcc = open(prefix + '-article-wcc-sz-cnt.txt', 'w')
# for item in wccDist:
#     wcc.write(str(item.GetVal1()))
#     wcc.write('\t')
#     wcc.write(str(item.GetVal2()))
#     wcc.write('\n')
#
# wcc.close()
#
# mxwcc = snap.GetMxWcc(G)
# mxwccFile = open(prefix + '-article-mxwcc.txt', 'w')
# for item in mxwcc.Edges():
#     mxwccFile.write(str(item.GetSrcNId()))
#     mxwccFile.write('\t')
#     mxwccFile.write(str(item.GetDstNId()))
#     mxwccFile.write('\n')
#
# mxwccFile.close()
#
# # Pagerank
# print 'pagerank...'
# pr = snap.TIntFltH()
# snap.GetPageRank(G, pr)
# pagerankFile = open(prefix + '-article-pagerank.txt', 'w')
# for item in pr:
#     pagerankFile.write(str(item))
#     pagerankFile.write('\t')
#     pagerankFile.write(str(pr[item]))
#     pagerankFile.write('\n')
#
# pagerankFile.close()
#
# # HITS
# print 'hits...'
# hub = snap.TIntFltH()
# auth = snap.TIntFltH()
# snap.GetHits(G, hub, auth)
# hubFile = open(prefix + '-article-hub.txt', 'w')
# for item in hub:
#     hubFile.write(str(item))
#     hubFile.write('\t')
#     hubFile.write(str(hub[item]))
#     hubFile.write('\n')
#
# hubFile.close()
#
# authFile = open(prefix + '-article-authority.txt', 'w')
# for item in auth:
#     authFile.write(str(item))
#     authFile.write('\t')
#     authFile.write(str(auth[item]))
#     authFile.write('\n')
#
# authFile.close()
#
# print 'done...'
#
